"""
Initial migration to create all core tables.
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender_enum') THEN
                CREATE TYPE gender_enum AS ENUM ('MALE', 'FEMALE');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS gender_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'training_type_enum') THEN
                CREATE TYPE training_type_enum AS ENUM(
                    'CARDIO', 'STRENGTH', 'FLEXIBILITY', 'BALANCE', 'HIIT', 'YOGA', 
                    'PILATES', 'ENDURANCE', 'CROSSFIT', 'FUNCTIONAL', 'REHABILITATION', 
                    'DANCE', 'SWIMMING', 'OTHER');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS training_type_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'intensity_enum') THEN
                CREATE TYPE intensity_enum AS ENUM(
                    'VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME');
            END IF;
        END $$;
        """
         "DROP TYPE IF EXISTS intensity_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'complexity_enum') THEN
                CREATE TYPE complexity_enum AS ENUM(
                    'BEGINNER', 'NOVICE', 'INTERMEDIATE', 'ADVANCED', 'EXPERT', 'MASTER');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS complexity_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'muscle_group_enum') THEN
                CREATE TYPE muscle_group_enum AS ENUM(
                    'CHEST', 'BACK', 'LEGS', 'ARMS', 'CORE', 'SHOULDERS', 
                    'BUTTOCKS', 'CALVES', 'NECK', 'HIPS', 'FULL_BODY', 'OTHER');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS muscle_group_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role_enum') THEN
                CREATE TYPE user_role_enum AS ENUM(
                    'ADMIN', 'USER', 'TRAINER', 'STAFFER', 'SYSTEM', 'ANALYST', 'OTHER');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS user_role_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'training_plan_status_enum') THEN
                CREATE TYPE training_plan_status_enum AS ENUM(
                    'PREPARED', 'ACTIVE', 'COMPLETED', 'DELAYED');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS training_plan_status_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'access_level_enum') THEN
                CREATE TYPE access_level_enum AS ENUM(
                    'LIMIT', 'STANDARD', 'PREMIUM', 'VIP', 'FAMILY', 'TRIAL', 
                    'DAY_PASS', 'WEEK_PASS', 'GUEST', 'CORPORATE', 'DISCOUNT', 'OTHER');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS access_level_enum;"
         ),

    step("""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'client_activity_status_enum') THEN
                CREATE TYPE client_activity_status_enum AS ENUM(
                    'ACTIVE', 'INACTIVE', 'ON_HOLD', 'CANCELLED', 'EXPIRED', 'UPCOMING');
            END IF;
        END $$;
        """,
         "DROP TYPE IF EXISTS client_activity_status_enum;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            role user_role_enum DEFAULT 'USER',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT NULL,
            deleted_at TIMESTAMP DEFAULT NULL
        );
        """,
         "DROP TABLE IF EXISTS Users;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Memberships (
            id SERIAL PRIMARY KEY,
            access_level access_level_enum DEFAULT 'STANDARD',
            description TEXT DEFAULT NULL,
            price NUMERIC(8, 2) NOT NULL
        );
        """,
         "DROP TABLE IF EXISTS Memberships;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Clients(
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE REFERENCES Users(id) ON DELETE NO ACTION,
            membership_id INTEGER NOT NULL REFERENCES Memberships(id) ON DELETE SET DEFAULT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            gender gender_enum,
            date_of_birth DATE NOT NULL,
            weight_kg NUMERIC(5, 2) DEFAULT NULL,
            height_cm NUMERIC(5, 2) DEFAULT NULL,
            status client_activity_status_enum DEFAULT 'ACTIVE'
        );
        """,
         "DROP TABLE IF EXISTS Clients;"
         ),

]
