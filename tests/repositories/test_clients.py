from datetime import date, datetime, timedelta

import pytest

from tests.conftest import get_repo
from trainings_app.brokers.consumer import get_system_user
from trainings_app.repositories.clients import ClientRepository

system_user = get_system_user()


@pytest.mark.asyncio
@pytest.mark.run(order=14)
async def test_create_client(get_repo):
    client_repo = get_repo(ClientRepository)
    client_data = {
        "user_id": 1,
        "membership_id": 1,
        "first_name": "Test client name",
        "last_name": "Test client last name",
        "phone_number": "+1234567890",
        "gender": "MALE",
        "date_of_birth": date(1999, 12, 15),
        "weight_kg": 99.1,
        "height_cm": 195.2,
        "status": "ACTIVE",
        "expiration_date": datetime.utcnow() + timedelta(days=30),
    }
    create_client = await client_repo.create(client_data)
    assert create_client is not None
    assert create_client.user_id == 1
    assert create_client.membership_id == 1
    assert create_client.id == 1
    assert create_client.phone_number == '+1234567890'
    assert create_client.status == "ACTIVE"


@pytest.mark.asyncio
@pytest.mark.run(order=15)
async def test_get_client(get_repo):
    client_repo = get_repo(ClientRepository)
    client_id = 1
    get_client = await client_repo.get(client_id)
    assert get_client is not None
    assert get_client.first_name == "Test client name"
    assert get_client.id == 1
    assert get_client.user_id == 1
    assert get_client.membership_id == 1


@pytest.mark.asyncio
@pytest.mark.run(order=16)
async def test_get_clients(get_repo):
    client_repo = get_repo(ClientRepository)
    filter_dict = {
        "first_name": "Test client name",
    }
    get_clients = await client_repo.get_clients(filter_dict)
    assert isinstance(get_clients, list)
    assert len(get_clients) == 1
    assert get_clients[0].first_name == "Test client name"
    assert get_clients[0].id == 1
    assert get_clients[0].user_id == 1
    assert get_clients[0].membership_id == 1


@pytest.mark.asyncio
@pytest.mark.run(order=17)
async def test_put_client(get_repo):
    client_repo = get_repo(ClientRepository)
    client_id = 1
    update_client_data = {
        "membership_id": 1,
        "first_name": "Updated FN",
        "last_name": "Updated LN",
        "phone_number": "+1234567890",
        "weight_kg": 99.5,
        "height_cm": 195.1,
        "status": "ACTIVE",
    }
    update_client = await client_repo.update(client_id, update_client_data, user=system_user)
    assert update_client is not None
    assert update_client.first_name == "Updated FN"
    assert update_client.last_name == "Updated LN"
    assert update_client.phone_number == "+1234567890"
    assert update_client.id == 1
    assert update_client.user_id == 1
    assert update_client.membership_id == 1


@pytest.mark.asyncio
@pytest.mark.run(order=18)
async def test_patch_client(get_repo):
    client_repo = get_repo(ClientRepository)
    client_id = 1
    update_client_data = {
        "phone_number": "+1230003335",
    }
    update_client = await client_repo.update(client_id, update_client_data, user=system_user)
    assert update_client is not None
    assert update_client.first_name == "Updated FN"
    assert update_client.last_name == "Updated LN"
    assert update_client.phone_number == "+1230003335"
    assert update_client.id == 1
    assert update_client.user_id == 1
    assert update_client.membership_id == 1


@pytest.mark.asyncio
@pytest.mark.run(order=19)
async def test_delete_client(get_repo):
    client_repo = get_repo(ClientRepository)
    extra_client_data = {
        "user_id": 3,
        "membership_id": 1,
        "first_name": "ExtraUser",
        "last_name": "ForDeleteTest",
        "phone_number": "+1234567890",
        "gender": "MALE",
        "date_of_birth": date(1988, 10, 25),
        "weight_kg": 99.1,
        "height_cm": 195.2,
        "status": "ACTIVE",
        "expiration_date": datetime.utcnow() + timedelta(days=30),
    }
    extra_client = await client_repo.create(extra_client_data)
    assert extra_client.id == 2
    extra_client_id = 2
    delete_client = await client_repo.delete(extra_client_id, user=system_user)
    assert delete_client is not None
    assert delete_client.id == 2
    assert delete_client.first_name == "ExtraUser"
