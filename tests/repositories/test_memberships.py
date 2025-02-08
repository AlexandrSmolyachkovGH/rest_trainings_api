import pytest

from tests.config_db_test import get_repo
from trainings_app.repositories.memberships import MembershipRepository

memberships_repo = get_repo(MembershipRepository)


@pytest.mark.asyncio
async def test_create_membership():
    memberships_data = {
        "access_level": "STANDARD",
        "description": "Standard access to services",
        "price": 199.99,
    }
    create_membership = await memberships_repo.create(memberships_data)
    assert create_membership is not None
    assert create_membership["access_level"] == "STANDARD"
    assert create_membership["price"] == 199.99
    assert create_membership["id"] > 0


@pytest.mark.asyncio
async def test_get_membership():
    membership_id = 1
    get_membership = await memberships_repo.get(membership_id)
    assert get_membership is not None
    assert get_membership["access_level"] == "STANDARD"
    assert get_membership["price"] == 199.99
    assert get_membership["id"] == 1


@pytest.mark.asyncio
async def test_get_memberships():
    filter_param = "STANDARD"
    get_memberships = memberships_repo.get_memberships(filter_param)
    assert isinstance(get_memberships, list)
    assert len(get_memberships) == 1
    assert get_memberships[0]["id"] == 1
    assert get_memberships[0]["price"] == 199.99


@pytest.mark.asyncio
async def test_put_membership():
    membership_id = 1
    update_membership_data = {
        "access_level": "VIP",
        "description": "Full access to all services",
        "price": 299.99,
    }
    update_membership = await memberships_repo.put(membership_id, update_membership_data)
    assert update_membership is not None
    assert update_membership["access_level"] == "VIP"
    assert update_membership["id"] == 1
    assert update_membership["price"] == 299.99


@pytest.mark.asyncio
async def test_patch_membership():
    membership_id = 1
    update_membership_data = {
        "description": "VIP: Full access to all services",
    }
    update_membership = await memberships_repo.patch(membership_id, update_membership_data)
    assert update_membership is not None
    assert update_membership["access_level"] == "VIP"
    assert update_membership["description"] == "VIP: Full access to all services"
    assert update_membership["id"] == 1


@pytest.mark.asyncio
async def test_delete_membership():
    extra_membership_data = {
        "access_level": "STANDARD",
        "description": "STANDARD: Standard access to services",
        "price": 199.99,
    }
    extra_membership = await memberships_repo.create(extra_membership_data)
    assert extra_membership["id"] == 2
    extra_membership_id = 2
    delete_membership = memberships_repo.delete(extra_membership_id)
    assert delete_membership is not None
    assert delete_membership["id"] == 2
    assert "STANDARD: " in delete_membership["description"]
