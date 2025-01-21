from trainings_app.db.fields.base import BaseFields


class TrainingExerciseFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list() -> list[str]:
        return ['training_id', 'exercise_id', 'order_in_training', 'sets', 'reps', 'rest_time_sec',
                'extra_weight']

    @classmethod
    def get_fields_str(cls) -> str:
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in TrainingExerciseFields.get_fields_list())
        return cls.cached_fields_str
