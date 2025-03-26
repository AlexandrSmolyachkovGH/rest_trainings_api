import unittest
from datetime import date
from pydantic import ValidationError

from trainings_app.schemas.clients import (
    CreateClient,
    GetClient,
    PutClient,
    GenderEnum,
    ClientStatusEnum,
)


class TestClientSchemas(unittest.IsolatedAsyncioTestCase):
    async def test_client_valid(self):
        """General validation tests for the Client entities."""
        test_cases = {
            "CreateClient": CreateClient,
            "GetClient": GetClient,
            "PutClient": PutClient,
        }
        for schema_name, schema in test_cases.items():
            client_data = {
                "user_id": 1,
                "membership_id": 10,
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+1234567890",
                "gender": GenderEnum.MALE,
                "date_of_birth": date(1990, 5, 20),
                "weight_kg": 70.5,
                "height_cm": 175.2,
                "status": ClientStatusEnum.INACTIVE,
                "expiration_date": "2024-12-25 00:00:00",
            }
            if schema_name != "CreateClient":
                client_data['id'] = 10
            if schema_name == "PutClient":
                client_data.pop('gender', GenderEnum.MALE)
            client = schema(**client_data)
            self.assertEqual(client.first_name, "John")
            self.assertEqual(client.status, ClientStatusEnum.INACTIVE)
            if hasattr(client_data, 'gender'):
                self.assertEqual(client.gender, GenderEnum.MALE)
            self.assertTrue(
                5 <= len(client.phone_number) <= 20,
                msg=f"Invalid length of the phone number: {len(client.phone_number)}."
            )
            valid_phone_chars = set("+0123456789")
            invalid_phone_chars = set(client.phone_number) - valid_phone_chars
            self.assertTrue(
                set(client.phone_number).issubset(valid_phone_chars),
                msg=f"Invalid phone number. Wrong symbols: {invalid_phone_chars}."
            )

    async def test_missing_required_fields(self):
        """Missing fields for the Client entities."""
        test_cases = {
            "CreateClient": CreateClient,
            "GetClient": GetClient,
            "PutClient": PutClient,
        }
        for schema_name, schema in test_cases.items():
            with self.subTest(schema=schema_name):
                with self.assertRaises(ValidationError, msg="Required fields are not specified."):
                    schema()

    async def test_enum_validation(self):
        with self.assertRaises(ValidationError):
            client = CreateClient(
                user_id=1,
                membership_id=10,
                first_name="John",
                last_name="Doe",
                phone_number="+1234567890",
                gender="INVALID GENDER",
                date_of_birth=date(1990, 5, 20),
                weight_kg=70.5,
                height_cm=175.2,
                status="INVALID STATUS"
            )
