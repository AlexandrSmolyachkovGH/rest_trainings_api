import dotenv
import os
from typing import Optional
import httpx
from pydantic import ValidationError

from trainings_app.repositories.base import BaseRepository
from trainings_app.db.fields.payments import PaymentFields
from trainings_app.schemas.payments import GetPayment, GetExtendedPaymentModel
from trainings_app.custom_loggers.repositories import repo_logger
from trainings_app.exceptions.exceptions import ConvertRecordError

dotenv.load_dotenv()


class PaymentRepository(BaseRepository):
    fields = PaymentFields

    @staticmethod
    def __get_payment_from_record(record: dict) -> GetPayment:
        """Retrieve GetPayment model from dict data"""

        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetPayment(**record)
        except ValidationError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail=f"{str(e)}")

    async def create(self, payment_data: dict) -> GetExtendedPaymentModel:
        keys, values, indexes = self.data_from_dict(payment_data)
        values_clause = ', '.join([f'${i}' for i in indexes])
        main_query = f"""
                INSERT INTO payments ({', '.join(keys)})
                VALUES ({values_clause})
                RETURNING {self.fields.get_fields_str()};
        """
        select_membership = f"""
                SELECT * 
                FROM memberships
                WHERE id = $1;
        """
        update_status_query = f"""
                UPDATE payments
                SET payment_status = $2
                WHERE id = $1
                RETURNING {self.fields.get_fields_str()};
        """
        async with self.conn.transaction():
            payment_record = dict(await self.fetchrow_or_404(main_query, *values))
            membership_data = dict(await self.conn.fetchrow(select_membership, payment_data['membership_id']))

            # Send the data to payment service
            async with httpx.AsyncClient() as client:
                payload = {
                    "client_id": payment_data['client_id'],
                    "amount": float(membership_data['price']),
                    "subscribe_type": membership_data['access_level']
                }
                response = await client.post(os.getenv('PAYMENT_SERVICE_URL'), json=payload)
                payment_link = (
                    ''.join(
                        [
                            os.getenv('PAY_URL'),
                            f"?id={response.json()['id']}",
                            f"&amount={response.json()['amount']}",
                        ]
                    )
                )
                status = 'FAILED' if response.status_code != 201 else 'PENDING'
            result = await self.conn.fetchrow(update_status_query, payment_record['id'], status)
            return GetExtendedPaymentModel(
                payment_data=self.__get_payment_from_record(result),
                payment_link=payment_link,
            )

    async def get(self, payment_id: int) -> GetPayment:
        query = f"""
            SELECT {self.fields.get_fields_str()} 
            FROM payments 
            WHERE id = $1;
        """
        payment_record = await self.fetchrow_or_404(query, payment_id)
        return self.__get_payment_from_record(payment_record)

    async def get_payments(self, filter_params: Optional[dict] = None) -> list[GetPayment]:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM payments
        """
        values = []
        if filter_params:
            keys, values, indexes = self.data_from_dict(filter_params)
            where_clause = ' AND '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
            query += f"""
                WHERE {where_clause}
            """
        query += ';'
        payment_data = await self.conn.fetch(query, *values)
        return [GetPayment(**pmt) for pmt in payment_data]

    async def delete(self, payment_id: int) -> GetPayment:
        query = f"""
            DELETE FROM payments
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        deleted_record = await self.fetchrow_or_404(query, payment_id)
        return self.__get_payment_from_record(deleted_record)

    async def update(self, payment_id: int, update_data: dict) -> GetPayment:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise ValidationError("Invalid update data")
        values.append(payment_id)
        set_clause = self.make_set_clause(keys=keys, indexes=indexes)
        query = f"""
            UPDATE payments
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {self.fields.get_fields_str()};
        """
        updated_record = await self.fetchrow_or_404(query, *values)
        return self.__get_payment_from_record(updated_record)
