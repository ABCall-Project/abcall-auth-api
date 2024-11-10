import unittest
from flaskr.application.auth_service import AuthService
from flaskr.domain.interfaces.AuthRepository import AuthRepository
from flaskr.domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
from unittest.mock import MagicMock, patch
from flaskr.domain.models import Auth


class TestAuthService(unittest.TestCase):
    def setUp(self):

        self.mock_auth_repository = MagicMock(spec=AuthRepository)
        self.mock_auth_user_customer_repository = MagicMock(spec=AuthUserCustomerRepository)
        

        self.auth_service = AuthService(
            auth_repository=self.mock_auth_repository,
            auth_user_customer_repository=self.mock_auth_user_customer_repository
        )

    def test_list_users_by_customer(self):

        customer_id = 1
        expected_users = ["user1", "user2"]
        self.mock_auth_user_customer_repository.list_users_by_customer.return_value = expected_users

        result = self.auth_service.list_users_by_customer(customer_id)
        self.assertEqual(result, expected_users)
        self.mock_auth_user_customer_repository.list_users_by_customer.assert_called_once_with(customer_id)

    def test_list_users_by_role(self):

        role_id = 2
        expected_users = ["user3", "user4"]
        self.mock_auth_repository.list_users_by_role.return_value = expected_users

        result = self.auth_service.list_users_by_role(role_id)
        self.assertEqual(result, expected_users)
        self.mock_auth_repository.list_users_by_role.assert_called_once_with(role_id)

    def test_get_company_by_user(self):
        user_id = 3
        expected_company = "CompanyA"
        self.mock_auth_user_customer_repository.get_company_by_user.return_value = expected_company

        result = self.auth_service.get_company_by_user(user_id)
        self.assertEqual(result, expected_company)
        self.mock_auth_user_customer_repository.get_company_by_user.assert_called_once_with(user_id)



    @patch('flaskr.application.auth_service.bcrypt.checkpw')
    def test_get_user_by_credentials_success(self, mock_checkpw):
        email = "test@example.com"
        password = "password123"
        hashed_password = "$2b$12$abcdefghijklmnopqrstuv"  

        mock_user = MagicMock(spec=Auth)
        mock_user.password = hashed_password
        self.mock_auth_repository.get_user_by_credentials.return_value = mock_user
        mock_checkpw.return_value = True

        result = self.auth_service.get_user_by_credentials(email, password)
        self.assertEqual(result, mock_user)
        self.mock_auth_repository.get_user_by_credentials.assert_called_once_with(email=email)
        mock_checkpw.assert_called_once_with(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @patch('flaskr.application.auth_service.bcrypt.checkpw')
    def test_get_user_by_credentials_invalid_password(self, mock_checkpw):
        email = "test@example.com"
        password = "wrong_password"
        hashed_password = "$2b$12$abcdefghijklmnopqrstuv"

        mock_user = MagicMock(spec=Auth)
        mock_user.password = hashed_password
        self.mock_auth_repository.get_user_by_credentials.return_value = mock_user
        mock_checkpw.return_value = False

        result = self.auth_service.get_user_by_credentials(email, password)
        self.assertIsNone(result)
        mock_checkpw.assert_called_once_with(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def test_hash_password(self):
        password = "password123"
        hashed_password = self.auth_service._AuthService__hash_password(password)

        self.assertIsInstance(hashed_password, str)
        self.assertTrue(hashed_password.startswith("$2b$"))

    @patch('flaskr.application.auth_service.bcrypt.checkpw')
    def test_check_password(self, mock_checkpw):
        password = "password123"
        hashed_password = "$2b$12$abcdefghijklmnopqrstuv"
        
        self.auth_service._AuthService__check_password(password, hashed_password)
        mock_checkpw.assert_called_once_with(password.encode('utf-8'), hashed_password.encode('utf-8'))
