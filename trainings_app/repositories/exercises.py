from typing import Optional

from trainings_app.db.fields.exercises import ExerciseFields
from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.exercises import CreateExercise, GetExercise, PutExercise, PatchExercise
from trainings_app.exceptions.exercises import ConvertExerciseRecordError, ExerciseNotFoundError, ExerciseAttrError


class ExerciseRepository(BaseRepository):
    @staticmethod
    def get_exercise_from_record(record: dict) -> GetExercise:
        """Retrieve GetTraining model from dict data"""
        if not record:
            raise ConvertExerciseRecordError("No record found to convert to GetTraining")
        return GetExercise(**record)

    async def create(self, arg: CreateExercise) -> GetExercise:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO exercises ({', '.join(keys)})
            VALUES ({', '.join([f"${i}" for i in indexes])})
            RETURNING {ExerciseFields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_exercise_from_record(record)

    async def get(self, exercise_id: int) -> GetExercise:
        query = f"""
            SELECT {ExerciseFields.get_fields_str()}
            FROM exercises
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, exercise_id)
        return self.get_exercise_from_record(record)

    async def get_exercises(self, filters: Optional[dict]) -> list[GetExercise]:
        values = []
        query = f"""
            SELECT {ExerciseFields.get_fields_str()}
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
            raise ExerciseNotFoundError(f"No relevant exercises error")
        return [GetExercise(**record) for record in records]

    async def delete(self, exercise_id: int) -> GetExercise:
        query = f"""
            DELETE FROM exercises
            WHERE id = $1
            RETURNING {ExerciseFields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, exercise_id)
        return self.get_exercise_from_record(record)

    async def update(self, exercise_id: int, update_data: dict) -> GetExercise:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            raise ExerciseAttrError("Invalid data for update")
        values.append(exercise_id)
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE exercises
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {ExerciseFields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.get_exercise_from_record(record)

