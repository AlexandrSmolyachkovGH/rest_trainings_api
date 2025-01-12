from typing import Optional

from trainings_app.repositories.base import BaseRepository, BaseFields
from trainings_app.schemas.trainings import CreateTraining, GetTraining, TrainingTypeEnum, IntensityEnum
from trainings_app.exceptions.trainings import TrainingsAttrError, TrainingNotFoundError, ConvertTrainingRecordError


class TrainingFields(BaseFields):
    @staticmethod
    def get_fields_list():
        return ['id', 'client_id', 'training_type', 'title', 'intensity', 'duration_min', 'date_of_train',
                'description']

    @staticmethod
    def get_fields_str():
        return ', '.join(field for field in TrainingFields.get_fields_list())


class TrainingRepository(BaseRepository):

    @staticmethod
    def get_training_from_record(record: dict) -> GetTraining:
        """Retrieve GetTraining model from dict data"""
        if not record:
            raise ConvertTrainingRecordError("No record found to convert to GetTraining")
        return GetTraining(**record)

    async def create(self, arg: CreateTraining) -> GetTraining:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO trainings {', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {TrainingFields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
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
            FORM trainings
        """
        if filters:
            keys, values, indexes = self.data_from_dict(filters)
            where_clause = ' AND '.join(f"{k} = {i}" for k, i in zip(keys, indexes))
            query += f"""
                WHERE {where_clause}
            """
        query += ";"
        records = await self.db.fetch(query, *values)
        if not records:
            raise TrainingNotFoundError(f"No relevant records error")
        return [GetTraining(record) for record in records]

    async def delete(self, train_id: int) -> GetTraining:
        query = f"""
            DELETE FROM trainings
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, train_id)
        return self.get_training_from_record(record)

    async def update(self, train_id: int, update_data: dict) -> GetTraining:
        keys, values, indexes = self.data_from_dict(update_data)
        values.append(train_id)
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE {TrainingFields.get_fields_str()}
            SET {set_clause}
            WHERE id = ${len(values)};            
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_training_from_record(record)
