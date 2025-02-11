import pytest
import pytest_asyncio

from tests.config_db_test import get_repo
from trainings_app.repositories.users import UserRepository


@pytest.mark.asyncio
@pytest.mark.run(order=1)
async def test_create_user(get_repo):
    user_repo = get_repo(UserRepository)
    user_data = {
        "username": "test001_user",
        "password_hash": "test001_user_password",
        "email": "test001_user@example.com",
        "role": "USER",
    }
    try:
        create_user = await user_repo.create(user_data)
        assert create_user is not None
        assert create_user["username"] == "test001_user"
        assert create_user["email"] == "test001_user@example.com"
        assert create_user["role"] == "USER"
        assert create_user["id"] > 0
    except Exception as e:
        pytest.fail(f"User creation failed: {e}")


@pytest.mark.asyncio
@pytest.mark.run(order=2)
async def test_get_user(get_repo):
    user_repo = get_repo(UserRepository)
    user_id = 1
    get_user = await user_repo.get(user_id)
    assert get_user is not None
    assert get_user["username"] == "test001_user"
    assert get_user["email"] == "test001_user@example.com"
    assert get_user["role"] == "USER"
    assert get_user["id"] > 0


@pytest.mark.asyncio
@pytest.mark.run(order=3)
async def test_get_users(get_repo):
    user_repo = get_repo(UserRepository)
    filter_dict = {
        "username": "test001_user",
    }
    get_users = user_repo.get_users(filter_dict)
    assert isinstance(get_users, list)
    assert len(get_users) == 1
    assert get_users[0]["username"] == "test001_user"
    assert get_users[0]["email"] == "test001_user@example.com"
    assert get_users[0]["role"] == "USER"


@pytest.mark.asyncio
@pytest.mark.run(order=4)
async def test_put_user(get_repo):
    user_repo = get_repo(UserRepository)
    user_id = 1
    update_user_data = {
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
@pytest.mark.run(order=5)
async def test_patch_user(get_repo):
    user_repo = get_repo(UserRepository)
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
@pytest.mark.run(order=6)
async def test_delete_user(get_repo):
    user_repo = get_repo(UserRepository)
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


@pytest.mark.asyncio
@pytest.mark.run(order=7)
async def test_extra_create_user(get_repo):
    user_repo = get_repo(UserRepository)
    user_data = {
        "username": "test003_user",
        "password_hash": "test003_user_password",
        "email": "test003_user@example.com",
        "role": "USER",
    }
    create_user = await user_repo.create(user_data)
    assert create_user is not None
    assert create_user["username"] == "test003_user"
    assert create_user["id"] == 3
