import unittest
from uuid import uuid4
from datetime import datetime
from flaskr.domain.models.auth import Auth


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.auth = Auth(
            id=self.sample_id,
            name="John",
            last_name="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            address="123 Main St",
            birthdate=datetime(1990, 1, 1),
            role_id="admin"
        )

    def test_init(self):
        self.assertEqual(self.auth.id, self.sample_id)
        self.assertEqual(self.auth.name, "John")
        self.assertEqual(self.auth.last_name, "Doe")
        self.assertEqual(self.auth.phone_number, "1234567890")
        self.assertEqual(self.auth.email, "john.doe@example.com")
        self.assertEqual(self.auth.address, "123 Main St")
        self.assertEqual(self.auth.birthdate, datetime(1990, 1, 1))
        self.assertEqual(self.auth.role_id, "admin")

    def test_to_dict(self):
        result = self.auth.to_dict()
        expected_dict = {
            'id': str(self.sample_id),
            'name': "John",
            'last_name': "Doe",
            'phone_number': "1234567890",
            'email': "john.doe@example.com",
            'address': "123 Main St",
            'birthdate': "1990-01-01",
            'role_id': "admin"
        }
        self.assertEqual(result, expected_dict)

    def test_to_dict_birthdate_none(self):
        self.auth.birthdate = None
        result = self.auth.to_dict()
        self.assertIsNone(result['birthdate'])
