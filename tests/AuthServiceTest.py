import unittest
import os
from unittest.mock import MagicMock, patch, Mock
from faker import Faker
from flaskr.application.auth_service import AuthService
from flaskr.domain.interfaces.AuthRepository import AuthRepository
from flaskr.domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
from builder.AuthBuilder import AuthBuilder
from mocks.repositories.auth_mock_repository import AuthMockRepository
from mocks.repositories.auth_customer_mock_repository import AuthCustomerMockRepository
from config import Config
from flaskr.domain.models import Auth
from flaskr.utils.encryption import generate_key_from_phrase, encrypt_data, base64_decode, encrypt_data_with_passphrase, base64_encode


class AuthServiceTestCase(unittest.TestCase):
    def setUp(self):

        self.mock_auth_repository = Mock(spec=AuthRepository)
        self.mock_auth_user_customer_repository = MagicMock(spec=AuthUserCustomerRepository)
        self.config = Config()
        

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
    
    @patch('flaskr.application.auth_service.Logger.info')
    def test_post_user_company(self, info_mock):
        message_expected = 'User created'
        faker = Faker()
        consumer_id = faker.uuid4()
        auth_mock = AuthBuilder().build()
        auth_mock_repository = AuthMockRepository()
        auth_user_customer_mock_repository = AuthCustomerMockRepository()
        auth_service = AuthService(auth_repository=auth_mock_repository, auth_user_customer_repository=auth_user_customer_mock_repository)

        auth_service.post_user_company(auth_mock, consumer_id)

        info_mock.assert_any_call(message_expected)
    
    @patch('flaskr.application.auth_service.Logger.warn')
    def test_post_user_company_return_an_error_when_the_exist(self, warn_mock):
        message_expected = 'User already exists'
        faker = Faker()
        consumer_id = faker.uuid4()
        auth_mock = AuthBuilder().build()
        auth_mock_repository = AuthMockRepository([])
        auth_user_customer_mock_repository = AuthCustomerMockRepository([])
        auth_mock_repository.create(auth_mock)
        auth_service = AuthService(auth_repository=auth_mock_repository, auth_user_customer_repository=auth_user_customer_mock_repository)
        try:
            auth_service.post_user_company(auth_mock, consumer_id)
        except ValueError as ex:
            self.assertEqual(str(ex), message_expected)
            warn_mock.assert_any_call(message_expected)


    def test_get_user_by_credentials_success(self):
        email = "test@example.com"
        password = "password123"
        salt = os.urandom(16)
        key = generate_key_from_phrase(self.config.PHRASE_KEY, salt)
        password_encrypt = encrypt_data(password,key)
        salt_decode = base64_encode(salt)
        user = AuthBuilder() \
            .with_password(password_encrypt) \
            .with_salt(salt_decode) \
            .build()
        self.mock_auth_repository.get_user_by_credentials.return_value = user
        password_sent = encrypt_data_with_passphrase(password, self.config.PHRASE_KEY)
        password_sent_decode = base64_encode(password_sent)

        result = self.auth_service.get_user_by_credentials(email, password_sent_decode)

        self.assertEqual(result, user)
 
    def test_get_user_by_credentials_invalid_password(self):
        email = "test@example.com"
        password = "wrong_password"
        real_password = "password123"
        salt = os.urandom(16)
        key = generate_key_from_phrase(self.config.PHRASE_KEY, salt)
        password_encrypt = encrypt_data(real_password,key)
        salt_decode = base64_encode(salt)
        user = AuthBuilder() \
            .with_password(password_encrypt) \
            .with_salt(salt_decode) \
            .build()
        self.mock_auth_repository.get_user_by_credentials.return_value = user
        password_sent = encrypt_data_with_passphrase(password, self.config.PHRASE_KEY)
        password_sent_decode = base64_encode(password_sent)
        
        result = self.auth_service.get_user_by_credentials(email, password_sent_decode)
        
        self.assertIsNone(result)
