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
         ),
    step("""
        CREATE TABLE IF NOT EXISTS Payments (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL,
            membership_id INTEGER NOT NULL,
            payment_status payment_status_enum default NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
         "DROP TABLE IF EXISTS Payments;"
         )
]
