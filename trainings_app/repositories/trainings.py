from fastapi import HTTPException, status
from typing import Optional

from trainings_app.db.fields.trainings import TrainingFields
from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.trainings import CreateTraining, GetTraining
from trainings_app.exceptions.exceptions import ConvertRecordError, RecordNotFoundError, AttrError
from trainings_app.logging.repositories import repo_logger


class TrainingRepository(BaseRepository):

    @staticmethod
    def get_training_from_record(record: dict) -> GetTraining:
        """Retrieve GetTraining model from dict data"""
        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, model_name="GetTraining", error_detail="No record found to convert")
        try:
            return GetTraining(**record)
        except Exception as e:
            repo_logger.error(f"Convert to model Error: {e}")
            raise ConvertRecordError(
                record=record, model_name="GetTraining", error_detail="Invalid data for conversion"
            )

    async def create(self, arg: CreateTraining) -> GetTraining:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO trainings ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {TrainingFields.get_fields_str()};
        """
        try:
            record = await self.fetchrow_or_404(query, *values)
        except Exception as e:
            repo_logger.error(f"Creation Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Training creation failed. Please try again later."
            )
        return self.get_training_from_record(record)

    async def get(self, train_id: int) -> GetTraining:
        query = f"""
            SELECT {TrainingFields.get_fields_str()}
            FROM trainings
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, train_id)
        return self.get_training_from_record(record)

    async def get_trainings(self, filters: Optional[dict] = None) -> list[GetTraining]:
        values = []
        query = f"""
            SELECT {TrainingFields.get_fields_str()}
            FROM trainings
        """
        if filters:
            keys, values, indexes = self.data_from_dict(filters)
            where_clause = ' AND '.join(f"{k} = ${i}" for k, i in zip(keys, indexes))
            query += f"""
                WHERE {where_clause}
            """
        query += ";"
        records = await self.db.fetch(query, *values)
        if not records:
            repo_logger.error(f"No relevant records Error")
            raise RecordNotFoundError(f"No relevant records error")
        return [GetTraining(**record) for record in records]

    async def delete(self, train_id: int) -> GetTraining:
        query = f"""
            DELETE FROM trainings
            WHERE id = $1
            RETURNING {TrainingFields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, train_id)
        return self.get_training_from_record(record)

    async def update(self, train_id: int, update_data: dict) -> GetTraining:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger("Invalid update data")
            raise AttrError("Invalid update data")
        values.append(train_id)
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE trainings
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {TrainingFields.get_fields_str()};            
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_training_from_record(record)
