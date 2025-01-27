from typing import Optional
from pydantic import ValidationError

from trainings_app.db.fields.trainings import TrainingFields
from trainings_app.db.fields.exercises import ExerciseFields
from trainings_app.repositories.base import BaseRepository
from trainings_app.schemas.trainings import CreateTraining, GetTraining
from trainings_app.exceptions.exceptions import ConvertRecordError
from trainings_app.logging.repositories import repo_logger


class TrainingRepository(BaseRepository):
    fields = TrainingFields

    @staticmethod
    def __get_training_from_record(record: dict) -> GetTraining:
        """Retrieve GetTraining model from dict data"""
        if not record:
            repo_logger.error(f"No record found to convert Error")
            raise ConvertRecordError(record=record, error_detail="No record found to convert")
        try:
            return GetTraining(**record)
        except ValidationError as e:
            repo_logger.error(f"Convert to model Error: {str(e)}")
            raise ConvertRecordError(record=record, error_detail=f"{str(e)}")

    async def create(self, arg: CreateTraining) -> GetTraining:
        keys, values, indexes = self.data_from_dict(arg)
        query = f"""
            INSERT INTO trainings ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.__get_training_from_record(record)

    async def get(self, train_id: int) -> GetTraining:
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM trainings
            WHERE id = $1;
        """
        record = await self.fetchrow_or_404(query, train_id)
        return self.__get_training_from_record(record)

    async def get_trainings(self, filters: Optional[dict] = None) -> list[GetTraining]:
        values = []
        query = f"""
            SELECT {self.fields.get_fields_str()}
            FROM trainings
        """
        if filters:
            keys, values, indexes = self.data_from_dict(filters)
            where_clause = ' AND '.join(f"{k} = ${i}" for k, i in zip(keys, indexes))
            query += f"""
                WHERE {where_clause}
            """
        query += ";"
        records = await self.conn.fetch(query, *values)
        return [GetTraining(**record) for record in records]

    async def delete(self, train_id: int) -> GetTraining:
        query = f"""
            DELETE FROM trainings
            WHERE id = $1
            RETURNING {self.fields.get_fields_str()};
        """
        record = await self.fetchrow_or_404(query, train_id)
        return self.__get_training_from_record(record)

    async def update(self, train_id: int, update_data: dict) -> GetTraining:
        keys, values, indexes = self.data_from_dict(update_data)
        if not values:
            repo_logger.error("Invalid update data")
            raise ValidationError("Invalid update data")
        values.append(train_id)
        set_clause = ', '.join([f"{k} = ${i}" for k, i in zip(keys, indexes)])
        query = f"""
            UPDATE trainings
            SET {set_clause}
            WHERE id = ${len(values)}
            RETURNING {self.fields.get_fields_str()};            
        """
        record = await self.fetchrow_or_404(query, *values)
        return self.__get_training_from_record(record)

    async def create_train_with_ex(self, data):
        train_data, ex_data = data[:-1], data[-1]
        keys, values, indexes = self.data_from_dict(train_data)
        query = f"""
            INSERT INTO trainings ({', '.join(keys)})
            VALUES ({', '.join([f'${i}' for i in indexes])})
            RETURNING {TrainingFields.get_fields_str()};
        """
        async with self.conn.transaction():
            train_record = await self.fetchrow_or_404(query, *values)
            created_train = GetTraining(**train_record)
            if ex_data:
                ex_keys, ex_values, ex_indexes = '', [], ''
                for exercise in ex_data:
                    keys, values, indexes = self.data_from_dict(exercise)
                    if not ex_keys:
                        ex_keys = f"""INSERT INTO trainings_exercises ({', '.join(keys)})
                        VALUES """
                    ex_indexes += f"({', '.join([f'${i}' for i in indexes])}),\n"
                    ex_values.append(*values)
                returning = f"\nRETURNING {ExerciseFields.get_fields_str()}"
                ex_query = ex_keys + ex_indexes.rstrip(',\n') + returning
                await self.conn.execute(ex_query, *ex_values)
                return created_train
