from trainings_app.db.fields.base import BaseFields


class ClientFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'user_id', 'membership_id', 'first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth',
                'weight_kg', 'height_cm', 'status', 'expiration_date']
