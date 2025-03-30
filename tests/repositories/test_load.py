import random
from datetime import date, datetime, timedelta

import pytest

from tests.conftest import get_repo
from trainings_app.repositories.clients import ClientRepository
from trainings_app.repositories.users import UserRepository


@pytest.mark.asyncio
@pytest.mark.run(order=20)
async def test_create_user(get_repo):
    user_repo = get_repo(UserRepository)
    clint_repo = get_repo(ClientRepository)
    for n in range(1, 100):

        user_data = {
            "username": f"test{n}_user",
            "password_hash": "test_password",
            "email": f"test{n}_user@example.com",
            "role": "USER",
        }
        try:
            create_user = await user_repo.create(user_data)
            assert create_user is not None
            assert create_user.username == f"test{n}_user"
            assert create_user.email == f"test{n}_user@example.com"
            assert create_user.role == "USER"
            assert create_user.id > 0
        except Exception as e:
            pytest.fail(f"User creation failed: {e}")

        client_data = {
            "user_id": create_user.id,
            "membership_id": 1,
            "first_name": f"TestUserFN_{create_user.id}",
            "last_name": f"TestUserLN_{create_user.id}",
            "phone_number": f"+1234567890{create_user.id}",
            "gender": ["MALE", "FEMALE"][random.randint(0, 1)],
            "date_of_birth": date(1988, 10, 25),
            "weight_kg": random.uniform(50, 100),
            "height_cm": random.uniform(150, 200),
            "status": "ACTIVE",
            "expiration_date": datetime.utcnow() + timedelta(days=30),
        }
        try:
            create_client = await clint_repo.create(client_data)
            assert create_client is not None
        except Exception as e:
            pytest.fail(f"User creation failed: {e}")
        print(f"Load Test {n} PASSED! - {datetime.utcnow()}")
