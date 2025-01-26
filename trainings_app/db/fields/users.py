from trainings_app.db.fields.base import BaseFields


class UserFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'username', 'password_hash', 'email', 'role', 'created_at', 'last_login', 'deleted_at']
