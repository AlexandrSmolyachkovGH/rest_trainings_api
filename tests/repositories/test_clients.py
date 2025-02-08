import pytest

from tests.config_db_test import get_repo
from trainings_app.repositories.users import UserRepository

user_repo = get_repo(UserRepository)


@pytest.mark.asyncio
async def test_create_user():
    user_data = {
        "username": "test001_user",
        "password_hash": "test001_user_password",
        "email": "test001_user@example.com",
        "role": "USER",
    }
    create_user = await user_repo.create(user_data)
    assert create_user is not None
    assert create_user["username"] == "test001_user"
    assert create_user["id"] > 0


@pytest.mark.asyncio
async def test_get_user():
    user_id = 1
    get_user = await user_repo.get(user_id)
    assert get_user is not None
    assert get_user["username"] == "test001_user"
    assert get_user["id"] == 1


@pytest.mark.asyncio
async def test_get_users():
    filter_dict = {
        "username": "test001_user",
    }
    get_users = user_repo.get_users(filter_dict)
    assert isinstance(get_users, list)
    assert len(get_users) == 1
    assert get_users[0]["username"] == "test001_user"


@pytest.mark.asyncio
async def test_put_user():
    user_id = 1
    update_user_data = {
        # "id": 1,  ???
        "username": "test01_user",
        "password_hash": "test01_user_password",
        "email": "test01_user@example.com",
        "role": "USER",
    }
    update_user = await user_repo.put(user_id, update_user_data)
    assert update_user is not None
    assert update_user["username"] == "test01_user"
    assert update_user["id"] == 1


@pytest.mark.asyncio
async def test_patch_user():
    user_id = 1
    update_user_data = {
        "password_hash": "test_user_password",
        "email": "test_user@example.com",
    }
    update_user = await user_repo.patch(user_id, update_user_data)
    assert update_user is not None
    assert update_user["username"] == "test01_user"
    assert update_user["id"] == 1


@pytest.mark.asyncio
async def test_delete_user():
    extra_user_data = {
        "username": "test002_user",
        "password_hash": "test002_user_password",
        "email": "test002_user@example.com",
        "role": "USER",
    }
    extra_user = await user_repo.create(extra_user_data)
    assert extra_user["id"] == 2
    extra_user_id = 2
    delete_user = user_repo.delete(extra_user_id)
    assert delete_user is not None
    assert delete_user["id"] == 2
    assert "002" in delete_user["username"]
