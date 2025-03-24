import httpx
from pydantic import ValidationError

from trainings_app.repositories.base import BaseRepository
from trainings_app.db.fields.payments import PaymentFields
from trainings_app.schemas.payments import GetPayment, GetExtendedPaymentModel
from trainings_app.custom_loggers.repositories import repo_logger
from trainings_app.exceptions.exceptions import ConvertRecordError
from trainings_app.settings import settings


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
        select_membership = f"""
                SELECT * 
                FROM memberships
                WHERE id = $1;
        """
        async with self.conn.transaction():
            membership_data = dict(await self.conn.fetchrow(select_membership, payment_data['membership_id']))
            # Send the data to payment service
            async with httpx.AsyncClient() as client:
                payload = {
                    "client_id": payment_data['client_id'],
                    "amount": float(membership_data['price']),
                    "subscribe_type": membership_data['access_level'],
                }
                response = await client.post(settings.payment_service_post_url, json=payload)
                response_data = response.json()
                payment_link = (
                    ''.join(
                        [
                            settings.payment_service_pay_page,
                            f"?id={response_data['id']}",
                            f"&amount={response_data['amount']}",
                        ]
                    )
                )
                result = GetExtendedPaymentModel(
                    payment_data=self.__get_payment_from_record(response_data),
                    payment_link=payment_link,
                )
                return result

    async def get(self):
        ...

    async def delete(self):
        ...

    async def update(self):
        ...
