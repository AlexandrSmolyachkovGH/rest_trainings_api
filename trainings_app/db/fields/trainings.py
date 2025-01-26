from trainings_app.db.fields.base import BaseFields


class TrainingFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'client_id', 'training_type', 'title', 'intensity', 'duration_min', 'date_of_train',
                'description']
