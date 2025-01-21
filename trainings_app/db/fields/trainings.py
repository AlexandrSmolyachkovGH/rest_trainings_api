from trainings_app.db.fields.base import BaseFields


class TrainingFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list() -> list[str]:
        return ['id', 'client_id', 'training_type', 'title', 'intensity', 'duration_min', 'date_of_train',
                'description']

    @classmethod
    def get_fields_str(cls) -> str:
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in TrainingFields.get_fields_list())
        return cls.cached_fields_str
