from trainings_app.db.fields.base import BaseFields


class ReportFields(BaseFields):
    cached_fields_str = None

    @classmethod
    def get_fields_list(cls) -> list[str]:
        return ['id', 'report_date_start', 'report_date_end', 'new_users']
