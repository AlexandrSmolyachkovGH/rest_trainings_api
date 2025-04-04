"""
Add payment table
"""

from yoyo import step

__depends__ = {'20250303_01_qx9M5'}

steps = [
    step("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'payment_status_enum') THEN
                    CREATE TYPE payment_status_enum AS ENUM ('PENDING', 'PAID', 'EXPIRED', 'CANCELLED', 'FAILED');
                END IF;
            END $$;
            """,
         "DROP TYPE IF EXISTS payment_status_enum;"
         )
]
