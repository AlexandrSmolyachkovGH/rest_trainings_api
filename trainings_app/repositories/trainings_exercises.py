from typing import Optional

from trainings_app.exceptions.exceptions import ConvertRecordError, AttrError, CreateRecordError
from trainings_app.logging.repositories import repo_logger
from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.trainings_exercises import CreateTrainingExercise, GetTrainingExercise
from trainings_app.db.fields.trainings_exercises import TrainingExerciseFields


class TrainingExerciseRepository(BaseRepository):
    fields = TrainingExerciseFields

    @staticmethod
    def get_model_from_record(record: dict) -> GetTrainingExercise:
        """Retrieve GetTrainingExercise model from dict data"""
        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetTrainingExercise(**record)
        except AttrError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail="Invalid data for conversion")

    async def create(self, arg: CreateTrainingExercise) -> GetTrainingExercise:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO trainings_exercises ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        try:
            record = await self.fetchrow_or_404(query, *values)
        except CreateRecordError as e:
            repo_logger.error(f"Creation Error: {str(e)}")
            raise CreateRecordError()
        return self.get_model_from_record(record)

    async def get(self, train_id: int, exercise_id: int) -> GetTrainingExercise:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM trainings_exercises
            WHERE training_id = $1 AND exercise_id = $2;
        """
        record = await self.fetchrow_or_404(query, train_id, exercise_id)
        return self.get_model_from_record(record)

    async def update(self, train_id: int, exercise_id: int, update_data: dict) -> GetTrainingExercise:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger("Invalid update data")
            raise AttrError("Invalid update data")
        values += [train_id, exercise_id]
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE trainings_exercises
            SET {set_clause}
            WHERE training_id = ${len(values) - 1} AND exercise_id = ${len(values)}
            RETURNING {self.fields.get_fields_str()};            
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_model_from_record(record)

    async def delete(self, train_id: int, exercise_id: int):
        query = f"""
            DELETE FROM trainings_exercises
            WHERE training_id = $1 AND exercise_id = $2
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, train_id, exercise_id)
        return self.get_model_from_record(record)

    async def get_trainings_exercises(self, filters: Optional[dict] = None) -> list[GetTrainingExercise]:
        values = []
        query = f"""
                    SELECT {self.fields.get_fields_str()}
                    FROM trainings_exercises
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
            return []
        return [GetTrainingExercise(**record) for record in records]
