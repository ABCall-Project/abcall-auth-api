import unittest
from unittest.mock import patch
from http import HTTPStatus
from flaskr.app import app
from flaskr.infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from flaskr.infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from builder.AuthBuilder import AuthBuilder
from builder.AuthUserCustomerBuilder import AuthUserCustomerBuilder

class AuthUserIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.auth_repository = AuthPostgresqlRepository()
        self.auth_user_customer_repository = AuthCustomerPostgresqlRepository()
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    
    def test_should_get_users_by_customer_id(self):
        auth = AuthBuilder().build()
        auth_customer = AuthUserCustomerBuilder().with_auth_user_id(auth.id).build()
        self.auth_repository.create(auth)
        self.auth_user_customer_repository.create(auth_customer)

        response = self.client.get(f'/users/getUsersByCustomer?customer_id={auth_customer.customer_id}', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)
    

