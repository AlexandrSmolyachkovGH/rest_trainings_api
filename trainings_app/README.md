## Training API Service

Is a **FastAPI-based backend** for managing clients, training sessions, exercises, reports and other entities in a
fitness
club. It includes:

- JWT Authentication (RSA-based, with Telegram verification);
- Client and Training Management;
- Exercise Catalog;
- Membership Handling;
- Automatic Reports Generation based on Celery;
- Implementation of payment processes by using RabbitMQ;
- And etc.

## Tech Stack

- `FastAPI` - Backend framework.
- `PostgreSQL` - Primary relational database.
- `Redis` - Caching & temporary data storage.
- `JWT (RSA)` - Authentication & token-based security.
- `Celery + RabbitMQ` - Background task processing & distributed task queue.
- `RabbitMQ (AMQP)` - Message broker for asynchronous communication.
- `Docker` - Containerization & service orchestration.

## Installation & Setup

...

## Authentication (JWT + Telegram)

To authenticate and obtain the necessary tokens, follow the instructions in `trainings_app/auth/README.md`.

## Database Schema

### Table Users

The table stores **Users Data** for using the service.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique user ID.
- `username` - `VARCHAR(50)` - **required, UNIQUE** - Username for the user account.
- `password_hash` - `VARCHAR(255)` - **required** - Hashed password for the user account.
- `email` - `VARCHAR(100)` - **required, UNIQUE** - User's email address.
- `role` - `ENUM` - **optional** - Specifies the user's role (for example, `ADMIN`, `USER`, `TRAINER`, etc.).
- `created_at` - `TIMESTAMP` - **optional** - The date and time when the user account was created. Default value is the
  current timestamp.
- `last_login` - `TIMESTAMP` - **optional** - The date and time of the user's last login. Default value is `NULL`.
- `deleted_at` - `TIMESTAMP` - **optional** - The date and time when the user account was deleted. Default value
  is `NULL`.

### Table Memberships

The table stores information about available **Memberships** in the app.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique membership ID.
- `access_level` - `ENUM` - **optional** - Specifies the membership (for example, `STANDARD`, `PREMIUM`, `VIP`).
- `description` - `TEXT` - **optional** - Additional information about membership.
- `price` - `NUMERIC` - **required** - Specific membership price.

### Table Clients

The table contains basic information about **the Clients** of the fitness club.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique client ID.
- `user_id` - `INTEGER` - **required, UNIQUE** - REFERENCES `Users(id)` - Links the client to relevant user. Foreign key
  with `ON DELETE NO ACTION`.
- `membership_id` - `INTEGER` - **required, UNIQUE** - REFERENCES `Memberships(id)` - Links the client to relevant
  membership. Foreign key with `ON DELETE SET DEFAULT`.
- `first_name` - `VARCHAR(50)` - **required** - Client's first name.
- `last_name` - `VARCHAR(80)` - **required** - Client's last name.
- `phone_number` - `VARCHAR(20)` - **required** - Client's phone number.
- `gender` - `ENUM` - **optional** - Gender of the client (for example, `MALE`, `FEMALE`).
- `date_of_birth` - `DATE` - **required** - Client's date of birth.
- `weight_kg` - `NUMERIC(5, 2)` - **optional** - Client's weight in kilograms.
- `height_sm` - `NUMERIC(5, 2)` - **optional** - Client's height in centimeters.
- `status` - `ENUM` - **optional** - Specifies client's current status (for example, `ACTIVE`, `INACTIVE`, `ON_HOLD`).
  Default value is `'ACTIVE'`.

### Table Trainings

The table contains information about **the client's Trainings**.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique training ID.
- `client_id` - `INTEGER` - **required** - REFERENCES `Clients(id)` - Indicates the client associated with the training
  record. Foreign key with `ON DELETE CASCADE`.
- `training_type` - `ENUM` - **optional** - Specifies the type of training (for example, `CARDIO`, `STRENGTH`, `YOGA`).
- `title` - `VARCHAR(200)` - **required** - Title of the training.
- `intensity` - `ENUM` - **optional** - Indicates the intensity of the training (for example, `LOW`, `MEDIUM`, `HIGH`).
- `duration_min` - `INTEGER` - **optional** - Training duration in minutes. Default value is `45`.
- `date` - `DATE` - **optional** - The date when the training took place. Default value is `NULL`.
- `description` - `TEXT` - **optional** - Additional information for a specific training. Default value is `NULL`.

### Table Exercises

The table contains information about **possible kinds of Exercises**.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique identifier for each exercise.
- `title` - `VARCHAR(50)` - **required, UNIQUE** - Unique name of the exercise.
- `description` - `TEXT` - **optional** - Detailed description of the exercise, including instructions or notes. Default
  value is `NULL`.
- `muscle_group` - `ENUM` - **optional** - Specifies the target muscle group for the exercise (for
  example, `CHEST`, `BACK`, `LEGS`, `ARMS`). Default value is `NULL`.
- `equipment_required` - `BOOLEAN` - **optional** - Indicates the necessity of equipment (`TRUE` for required, `FALSE`
  for no equipment needed). Default value is `FALSE`.
- `complexity_lvl` - `ENUM` - **optional** - Indicates the complexity level of exercise (for
  example, `INTERMEDIATE`, `ADVANCED`, `EXPERT`). Default value is `BEGINNER`.

### Table Trainings_exercises

The table **links tables Exercises and Trainings** and provides additional information about their configuration.

- `training_id` - `INTEGER` - **required** - REFERENCES `Trainings(id)` - The training that includes certain exercise.
  Foreign key with `ON DELETE CASCADE`.
- `exercise_id` - `INTEGER` - **required** - REFERENCES `Exercises(id)` - The exercise that is included in certain
  training. Foreign key with `ON DELETE CASCADE`.
- `order_in_training` - `INTEGER` - **required** - Specifies the queue number of this exercise within the training.
- `sets` - `INTEGER` - **optional** - Number of sets for the exercise. Default value is `3`.
- `reps` - `INTEGER` - **optional** - Number of repetitions per set. Default value is `10`.
- `rest_time_sec` - `INTEGER` - **optional** - Rest time between sets in seconds. Default value is `60`.
- `extra_weight` - `NUMERIC(5, 2)` - **optional** - Additional weight (in kilograms) used for the exercise. Default
  value is `NULL`.

### Table Training_plans

The table contains information about the client's **specific training plan**.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique training plan identifier.
- `user_id` - `INTEGER` - **required** - REFERENCES `Users(id)` - The user ID associated with specific training plan.
- `title` - `VARCHAR(200)` - **required** - Name of the training plan.
- `description` - `TEXT` - **optional** - Detailed description of the training plan. Default value is `NULL`.
- `created_at` - `TIMESTAMP` - **optional** - The date and time when the training plan was created. Default value
  is `CURRENT_TIMESTAMP`.
- `status` - `ENUM` - **optional** - Specifies the plan status (for example, `PREPARED`, `ACTIVE`, `COMPLETED`). Default
  value is `ACTIVE`.

### Table Training_plan_trainings

The table **links tables Trainings and Training_plans**.

- `training_id` - `INTEGER` - **required** - REFERENCES `Trainings(id)` - The training ID included in a specific plan.
  Foreign key with `ON DELETE CASCADE`.
- `training_plan_id` - `INTEGER` - **required** - REFERENCES `Training_plans(id)` - The plan ID refers to specific
  trainings. Foreign key with `ON DELETE CASCADE`.

### Table Clients_training_plan

The table **links tables Clients and Training_plans**.

- `client_id` - `INTEGER` - **required** - REFERENCES `Clients(id)` - The client ID included in a specific plan.
  Foreign key with `ON DELETE CASCADE`.
- `training_plan_id` - `INTEGER` - **required** - REFERENCES `Training_plans(id)` - The plan ID refers to a specific
  client. Foreign key with `ON DELETE CASCADE`.
- `pinned_at` - `TIMESTAMP` - **optional** - Specifies the time of addition. Default value is `CURRENT_TIMESTAMP`.

### Table Simple_Report

The table stores **report content** and additional information.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique identifier of the report.
- `report_date_start` - `DATE` - **required** - Start date of report.
- `report_date_end` - `DATE` - **required** - End date of report.
- `new_users` - `JSONB` - **required** - Report payload.

### Table Payments

The table contains detailed **payment information** included payment statuses and etc.

- `id` - `SERIAL PRIMARY KEY` - **required** - Unique identifier of the payment.
- `client_id` - `INTEGER` - **required** - Client ID referring to the payment.
- `membership_id` - `INTEGER` - **required** - Membership ID referring to the payment.
- `payment_status` - `ENUM` - **optional** - Indicates the status of the payment (for
  example, `PENDING`, `PAID`, `EXPIRED`). Default value is `NULL`.
- `timestamp` - `TIMESTAMP` - **optional** - Timestamp of the specified payment status.

## API Endpoints

### API Access Levels

Description of the possible **access types** for routes:

- `Unauthenticated` – Routes that do not require authentication and are accessible to all users.
- `Authenticated` - Routes that require basic user authentication and are accessible to authorized users.
- `Restricted` - Routes that require elevated access permissions and are accessible only to users with administrator
  roles.

### Index

- `GET` - `/` - **Unauthenticated** - Returns base information of the service.

### Health

- `GET` - `/health/` - **Unauthenticated** - Returns the running status of the service.

### Authentication

`POST` - `/jwt-auth/login/` - **Unauthenticated** - Login & get Telegram verification link.
`POST` - `/jwt-auth/verification/` - **Unauthenticated** - Verify Telegram code & get refresh token.
`POST` - `/jwt-auth/get-access-token/` - **Unauthenticated** - Exchange refresh token for access token.

### Users

- `GET` - `/users/` - **Restricted** - Retrieve list of users.
- `GET` - `/users/{user_id}/` - **Authenticated** - Retrieve the user by ID.
- `GET` - `/users/for-report/` - **Authenticated** - Retrieve list of users for a report.
- `POST` - `/users/` - **Unauthenticated** - Create the user.
- `DELETE` - `/users/{user_id}/` - **Authenticated** - Delete the user.
- `PUT` - `/users/{user_id}/` - **Authenticated** - Complete update of the user record.
- `PATCH` - `/users/{user_id}/` - **Authenticated** - Partial update of the user record.

### Memberships

- `GET` - `/memberships/` - **Restricted** - Retrieve list of memberships
- `GET` - `/memberships/{membership_id}/` - **Restricted** - Retrieve the membership by ID.
- `POST` - `/memberships/` - **Restricted** - Create the membership.
- `DELETE` - `/memberships/{membership_id}/` - **Restricted** - Delete the membership.
- `PUT` - `/memberships/{membership_id}/` - **Restricted** - Complete update of the membership record.
- `PATCH` - `/memberships/{membership_id}/` - **Restricted** - Partial update of the membership record.

### Clients

- `GET` - `/clients/` - **Restricted** - Retrieve list of clients.
- `GET` - `/clients/{client_id}/` - **Authenticated** - Retrieve the client by ID.
- `POST` - `/clients/` - **Authenticated** - Create the client.
- `DELETE` - `/clients/{client_id}/` - **Authenticated** - Delete the client.
- `PUT` - `/clients/{client_id}/` - **Authenticated** - Complete update of the client record.
- `PATCH` - `/clients/{client_id}/` - **Authenticated** - Partial update of the client record.

### Trainings

- `GET` - `/trainings/` - **Restricted** - Retrieve list of trainings.
- `GET` - `/trainings/{train_id}/` - **Authenticated** - Retrieve the training by ID.
- `GET` - `/trainings/exercice-ids/{train_id}/` - **Authenticated** - Retrieve the training with exercise IDs.
- `POST` - `/trainings/` - **Authenticated** - Create the training.
- `POST` - `/trainings/exercice-ids/` - **Authenticated** - Create the training with indicated exercises.
- `DELETE` - `/trainings/{train_id}/` - **Authenticated** - Delete the training.
- `PUT` - `/trainings/{train_id}/` - **Authenticated** - Complete update of the training record.
- `PATCH` - `/trainings/{train_id}/` - **Authenticated** - Partial update of the training record.

### Trainings-exercises

- `GET` - `/trainings-exercises/` - **Restricted** - Retrieve training-exercise records.
- `GET` - `/trainings-exercises/{training_id}/{exercise_id}/` - **Authenticated** - Retrieve the training-exercise
  record.
- `POST` - `/trainings-exercises/` - **Authenticated** - Create the training-exercise record.
- `DELETE` - `/trainings-exercises/{exercise_id}/` - **Authenticated** - Delete the training-exercise record.
- `PUT` - `/trainings-exercises/{exercise_id}/` - **Authenticated** - Complete update of the training-exercise record.
- `PATCH` - `/trainings-exercises/{exercise_id}/` - **Authenticated** - Partial update of the training-exercise record.

### Payments

- `GET` - `/payments/` - **Restricted** - Retrieve list of payments.
- `GET` - `/payments/{payment_id}/` - **Authenticated** - Retrieve the payment by ID.
- `POST` - `/payments/` - **Authenticated** - Create the payment record.
- `DELETE` - `/payments/{payment_id}/` - **Authenticated** - Delete the payment record.
- `PUT` - `/payments/{payment_id}/` - **Authenticated** - Complete update of the payment record.

### Reports

- `POST` - `/payments/` - **Authenticated** - Add information for daily report.









