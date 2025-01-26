from trainings_app.db.fields.base import BaseFields


class ExerciseFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'title', 'description', 'muscle_group', 'equipment_required', 'complexity_lvl']
