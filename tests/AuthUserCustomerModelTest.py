import unittest
from uuid import uuid4, UUID
from flaskr.domain.models.auth_user_customer import AuthUserCustomer

class TestAuthUserCustomer(unittest.TestCase):
    def setUp(self):
        self.sample_id = uuid4()
        self.sample_auth_user_id = uuid4()
        self.sample_customer_id = uuid4()
        self.auth_user_customer = AuthUserCustomer(
            id=self.sample_id,
            auth_user_id=self.sample_auth_user_id,
            customer_id=self.sample_customer_id
        )

    def test_init(self):
        self.assertEqual(self.auth_user_customer.id, self.sample_id)
        self.assertEqual(self.auth_user_customer.auth_user_id, self.sample_auth_user_id)
        self.assertEqual(self.auth_user_customer.customer_id, self.sample_customer_id)

    def test_to_dict(self):
        result = self.auth_user_customer.to_dict()
        expected_dict = {
            'id': str(self.sample_id),
            'auth_user_id': str(self.sample_auth_user_id),
            'customer_id': str(self.sample_customer_id)
        }
        self.assertEqual(result, expected_dict)

    def test_to_dict_contains_correct_types(self):
        result = self.auth_user_customer.to_dict()
        self.assertIsInstance(result['id'], str)
        self.assertIsInstance(result['auth_user_id'], str)
        self.assertIsInstance(result['customer_id'], str)
