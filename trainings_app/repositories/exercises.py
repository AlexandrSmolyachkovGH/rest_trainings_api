from typing import Optional

from trainings_app.db.fields.exercises import ExerciseFields
from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.exercises import CreateExercise, GetExercise
from trainings_app.logging.repositories import repo_logger
from trainings_app.exceptions.exceptions import ConvertRecordError, AttrError, CreateRecordError


class ExerciseRepository(BaseRepository):
    fields = ExerciseFields

    @staticmethod
    def get_exercise_from_record(record: dict) -> GetExercise:
        """Retrieve GetTraining model from dict data"""
        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetExercise(**record)
        except AttrError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail="Invalid data for conversion")

    async def create(self, arg: CreateExercise) -> GetExercise:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO exercises ({', '.join(keys)})
            VALUES ({', '.join([f"${i}" for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        try:
            record = await self.db.fetchrow(query, *values)
        except CreateRecordError as e:
            repo_logger.error(f"Creation Error: {str(e)}")
            raise CreateRecordError()
        return self.get_exercise_from_record(record)

    async def get(self, exercise_id: int) -> GetExercise:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM exercises
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, exercise_id)
        return self.get_exercise_from_record(record)

    async def get_exercises(self, filters: Optional[dict]) -> list[GetExercise]:
        values = []
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM exercises
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
        return [GetExercise(**record) for record in records]

    async def delete(self, exercise_id: int) -> GetExercise:
        query = f"""
            DELETE FROM exercises
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, exercise_id)
        return self.get_exercise_from_record(record)

    async def update(self, exercise_id: int, update_data: dict) -> GetExercise:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error(f"Invalid update data")
            raise AttrError("Invalid update data")
        values.append(exercise_id)
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE exercises
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_exercise_from_record(record)
