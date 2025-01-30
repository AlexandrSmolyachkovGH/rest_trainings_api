import unittest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from trainings_app.schemas.clients import GetClient, CreateClient, PutClient, PatchClient, ClientFilters, GenderEnum, \
    ClientStatusEnum
from trainings_app.repositories.clients import ClientRepository


class TestClientRepository(unittest.IsolatedAsyncioTestCase):

    async def setUp(self):
        self.mock_session = AsyncMock()
        self.repo = ClientRepository(self.mock_session)

    @unittest.mock.patch.object(ClientRepository, 'fetchrow_or_404')
    async def test_get_client(self, mock_fetchrow_or_404):
        mock_fetchrow_or_404.return_value = {
            'id': 85,
            'user_id': 115,
            'membership_id': 41,
            'first_name': 'Test',
            'last_name': 'Mock',
            'phone_number': '+14598881420',
            'gender': GenderEnum.MALE,
            'date_of_birth': "1982-12-25",
            'weight_kg': 82,
            'height_cm': 179,
            'status': ClientStatusEnum.ACTIVE,
        }
        self.assertIsInstance(self.repo, ClientRepository)
        client = await self.repo.get(85)

        self.assertEqual(client.id, 85)
        self.assertTrue(
            all(v > 0 for v in [client.id, client.user_id, client.membership_id, client.weight_kg, client.height_cm])
        )
        self.assertTrue(1900 < client.date_of_birth.year <= datetime.now().year)


if __name__ == '__main__':
    unittest.main()
