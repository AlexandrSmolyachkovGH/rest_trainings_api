from trainings_app.db.fields.base import BaseFields


class MembershipFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'access_level', 'description', 'price']
