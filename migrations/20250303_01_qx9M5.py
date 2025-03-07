"""
Migrations for Report entities
"""

from yoyo import step

__depends__ = {'20250112_01_ZfOxG-add-trainings-tables'}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS Simple_Report (
            id SERIAL PRIMARY KEY,
            report_date_start DATE NOT NULL,
            report_date_end DATE NOT NULL,
            new_users JSONB
        );
        """,
         "DROP TABLE IF EXISTS Simple_Report;"
         )
]
