from trainings_app.db.fields.base import BaseFields


class MembershipFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list():
        return ['id', 'access_level', 'description', 'price']

    @classmethod
    def get_fields_str(cls):
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in MembershipFields.get_fields_list())
        return cls.cached_fields_str
