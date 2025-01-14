from trainings_app.db.fields.base import BaseFields


class UserFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list():
        return ['id', 'username', 'password_hash', 'email', 'role', 'created_at', 'last_login', 'deleted_at']

    @classmethod
    def get_fields_str(cls):
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in UserFields.get_fields_list())
        return cls.cached_fields_str
