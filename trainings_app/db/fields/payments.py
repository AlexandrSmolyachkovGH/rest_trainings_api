from trainings_app.db.fields.base import BaseFields


class PaymentFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['client_id', 'membership_id', 'payment_status']
