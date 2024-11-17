import unittest
from flaskr.domain.interfaces.AuthRepository import AuthRepository


class AuthRepositoryUseCase(unittest.TestCase):

    def setUp(self):
        self.repo = AuthRepository()

    def test_list_users_by_role_implementation(self, page=None,limit=None):
        with self.assertRaises(NotImplementedError):
            self.repo.list_users_by_role(role_id=None)
    
    def test_create_implementation(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create(user=None)
            