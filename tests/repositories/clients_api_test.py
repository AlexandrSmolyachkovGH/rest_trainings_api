import unittest
import asyncio
import asyncpg
import httpx
from yoyo import read_migrations, get_backend

from trainings_app.main import app
from trainings_app.schemas.clients import GetClient
from trainings_app.settings import settings_test_db
from trainings_app.repositories.clients import ClientRepository


class TestClientsAPI(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        backend = get_backend(settings_test_db.postgres_dsn)
        migrations = read_migrations("../../migrations")
        with backend.lock():
            backend.apply_migrations(migrations)
        cls.loop = asyncio.get_event_loop()
        cls.pool = cls.loop.run_until_complete(asyncpg.create_pool(settings_test_db.postgres_dsn))
        cls.client = httpx.AsyncClient(app=app, base_url="http://test")
        cls.repo = ClientRepository(cls.pool)

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(cls.client.aclose())
        backend = get_backend(settings_test_db.postgres_dsn)
        migrations = read_migrations("migrations")
        with backend.lock():
            backend.rollback_migrations(migrations)
        cls.loop.run_until_complete(cls.pool.close())

    async def test_create(self):
        client_data = {
            "user_id": 1,
            "membership_id": 1,
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "+1234567890",
            "gender": "MALE",
            "date_of_birth": "2000-12-25",
        }
        created_client = await self.repo.create(client_data)
        self.assertTrue(isinstance(created_client, GetClient))
        self.assertTrue(created_client.model_dump()[''] == client_data[''])


if __name__ == '__main__':
    unittest.main()
