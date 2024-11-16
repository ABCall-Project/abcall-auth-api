import unittest
from flaskr.domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository


class AuthUserCompanyRepositoryUseCase(unittest.TestCase):

    def setUp(self):
        self.repo = AuthUserCustomerRepository()

    def test_list_users_by_customer_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.list_users_by_customer(customer_id=None)
    
    def test_get_company_by_user_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.get_company_by_user(user_id=None)
    
    def test_create_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create(user=None)
            