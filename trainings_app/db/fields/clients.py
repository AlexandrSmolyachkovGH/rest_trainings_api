from trainings_app.db.fields.base import BaseFields


class ClientFields(BaseFields):
    cached_fields_str = None

    @staticmethod
    def get_fields_list():
        return ['id', 'user_id', 'membership_id', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth',
                'weight_kg', 'height_cm', 'status']

    @classmethod
    def get_fields_str(cls):
        if cls.cached_fields_str is None:
            cls.cached_fields_str = ', '.join(field for field in ClientFields.get_fields_list())
        return cls.cached_fields_str
