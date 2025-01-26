from trainings_app.db.fields.base import BaseFields


class TrainingExerciseFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['training_id', 'exercise_id', 'order_in_training', 'sets', 'reps', 'rest_time_sec',
                'extra_weight']
