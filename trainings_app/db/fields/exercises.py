from trainings_app.db.fields.base import BaseFields


class ExerciseFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list():
        return ['id', 'title', 'description', 'muscle_group', 'equipment_required', 'complexity_lvl']

    @classmethod
    def get_fields_str(cls):
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in ExerciseFields.get_fields_list())
        return cls.cached_fields_str
