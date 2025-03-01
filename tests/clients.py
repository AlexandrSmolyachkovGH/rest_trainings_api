import unittest
import os
from unittest.mock import AsyncMock, patch

from trainings_app.schemas.clients import GetClient, GenderEnum, ClientStatusEnum
from trainings_app.repositories.clients import ClientRepository


class TestClientRepository(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.create_input_data = {
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
        cls.create_db_response = {
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

    async def asyncSetUp(self):
        self.repo = ClientRepository(None)

    @patch.object(ClientRepository, 'create', new_callable=AsyncMock)
    async def test_create_client_success(self, mock_create):
        mock_create.return_value = GetClient(**TestClientRepository.create_db_response)
        created_client = await self.repo.create(TestClientRepository.create_input_data)
        self.assertIsInstance(created_client, GetClient)
        self.assertEqual(created_client.dict()['id'], 85)



if __name__ == '__main__':
    unittest.main()
