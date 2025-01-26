"""
add_trainings_tables
"""

from yoyo import step

__depends__ = {'20241222_add_base_tables'}

steps = [
    step("""
        CREATE TABLE IF NOT EXISTS Trainings (
            id SERIAL PRIMARY KEY,
            client_id INTEGER NOT NULL REFERENCES Clients(id) ON DELETE CASCADE,
            training_type training_type_enum DEFAULT NULL,
            title VARCHAR(200) NOT NULL,
            intensity intensity_enum DEFAULT NULL,
            duration_min INTEGER DEFAULT 45,
            date_of_train DATE DEFAULT NULL,
            description TEXT DEFAULT NULL
            
        );
        """
         "DROP TABLE IF EXISTS Trainings;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Exercises (
            id SERIAL PRIMARY KEY,
            title VARCHAR(50) NOT NULL UNIQUE,
            description TEXT DEFAULT NULL,
            muscle_group muscle_group_enum DEFAULT NULL,
            equipment_required BOOLEAN DEFAULT FALSE,
            complexity_lvl complexity_enum DEFAULT 'BEGINNER'
        );
        """
         "DROP TABLE IF EXISTS Exercises;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Trainings_exercises (
            training_id INTEGER NOT NULL REFERENCES Trainings(id) ON DELETE CASCADE,
            exercise_id INTEGER NOT NULL REFERENCES Exercises(id) ON DELETE CASCADE,
            order_in_training INTEGER NOT NULL,
            sets INTEGER DEFAULT 3,
            reps INTEGER DEFAULT 10,
            rest_time_sec INTEGER DEFAULT 60,
            extra_weight NUMERIC(5, 2) DEFAULT NULL,
            PRIMARY KEY (training_id, exercise_id)
        );
        """
         "DROP TABLE IF EXISTS Trainings_exercises;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Training_plans (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
            title VARCHAR(200) NOT NULL,
            description TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status training_plan_status_enum DEFAULT 'ACTIVE'
        );
        """
         "DROP TABLE IF EXISTS Training_plans;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Training_plan_trainings (
            training_id INTEGER NOT NULL REFERENCES Trainings(id) ON DELETE CASCADE,
            training_plan_id INTEGER NOT NULL REFERENCES Training_plans(id) ON DELETE CASCADE,
            PRIMARY KEY (training_id, training_plan_id)
        );
        """
         "DROP TABLE IF EXISTS Training_plan_trainings;"
         ),

    step("""
        CREATE TABLE IF NOT EXISTS Clients_training_plan (
            client_id INTEGER NOT NULL REFERENCES Clients(id) ON DELETE CASCADE,
            training_plan_id INTEGER NOT NULL REFERENCES Training_plans(id) ON DELETE CASCADE,
            pinned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (client_id, training_plan_id)
        );
        """
         "DROP TABLE IF EXISTS Clients_training_plan;"
         ),

]
