"""
Initial migration to create all core tables.
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        create type gender_enum as ENUM ('MALE', 'FEMALE');
        CREATE TABLE Clients(
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE REFERENCES Users(id) ON DELETE CASCADE,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(80) NOT NULL,
            email VARCHAR(100) DEFAULT NULL,
            phone_number VARCHAR(20) NOT NULL,
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            type_of_membership VARCHAR(50) DEFAULT 'STANDART',
            gender gender_enum  DEFAULT NULL,
            date_of_birth DATE NOT NULL,
            weight_kg NUMERIC(5, 2) DEFAULT NULL,
            height_cm NUMERIC(5, 2) DEFAULT NULL,
            status VARCHAR(15) DEFAULT 'ACTIVE',
            membership_id INTEGER NOT NULL REFERENCES Memberships(id)
        );

        create type training_type_enum as ENUM('CARDIO', 'STRENGTH', 'FLEXIBILITY', 'BALANCE', 'HIIT', 'YOGA', 'PILATES', 'ENDURANCE', 'CROSSFIT', 'FUNCTIONAL', 'REHABILITATION', 'DANCE', 'SWIMMING', 'OTHER');
        create type intensity_enum as ENUM('VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH', 'EXTREME');
        CREATE TABLE Trainings (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES Clients(id) ON DELETE CASCADE,
            training_type training_type_enum DEFAULT NULL,
            title VARCHAR(200) NOT NULL,
            intensity intensity_enum DEFAULT NULL,
            duration_min INTEGER DEFAULT 45,
            date DATE DEFAULT NULL,
            description TEXT DEFAULT NULL
        );
        create type complexity_enum as ENUM('BEGINNER', 'NOVICE', 'INTERMEDIATE', 'ADVANCED', 'EXPERT', 'MASTER');
        create type muscle_group_enum as ENUM('CHEST', 'BACK', 'LEGS', 'ARMS', 'CORE', 'SHOULDERS', 'BUTTOCKS', 'CALVES', 'NECK', 'HIPS', 'FULL_BODY', 'OTHER');
        CREATE TABLE Exercises (
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL UNIQUE,
            description TEXT DEFAULT NULL,
            muscle_group muscle_group_enum DEFAULT NULL,
            equipment_required BOOLEAN DEFAULT FALSE,
            complexity_lvl complexity_enum DEFAULT 'BEGINNER'
        );
        CREATE TABLE Trainings_exercises (
            training_id INTEGER NOT NULL REFERENCES Trainings(id) ON DELETE CASCADE,
            exercise_id INTEGER NOT NULL REFERENCES Exercises(id) ON DELETE CASCADE,
            order_in_training INTEGER NOT NULL,
            sets INTEGER DEFAULT 3,
            reps INTEGER DEFAULT 10,
            rest_time_sec INTEGER DEFAULT 60,
            extra_weight NUMERIC(5, 2) DEFAULT NULL,
            PRIMARY KEY (training_id, exercise_id)
        );
        create type user_role_enum as ENUM('ADMIN', 'USER', 'TRAINER', 'STAFFER', 'SYSTEM', 'ANALYST', 'OTHER');
        CREATE TABLE Users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            role user_role_enum DEFAULT 'USER',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT NULL,
            deleted_at TIMESTAMP DEFAULT NULL
        );
        create type train_status_enum as ENUM ('PREPARED', 'ACTIVE', 'COMPLETED', 'DELAYED');
        CREATE TABLE Training_plans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
            title VARCHAR(200) NOT NULL,
            description TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status train_status_enum DEFAULT 'ACTIVE'
        );
        CREATE TABLE Training_plan_trainings (
            training_id INTEGER NOT NULL REFERENCES Trainings(id) ON DELETE CASCADE,
            training_plan_id INTEGER NOT NULL REFERENCES Training_plans(id) ON DELETE CASCADE,
            PRIMARY KEY (training_id, training_plan_id)
        );
        CREATE TABLE Clients_training_plan (
            client_id INTEGER NOT NULL REFERENCES Clients(id) ON DELETE CASCADE,
            training_plan_id INTEGER NOT NULL REFERENCES Training_plans(id) ON DELETE CASCADE,
            pinned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (client_id, training_plan_id)
        );
        CREATE TABLE Memberships (
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
        );
    """)
]
