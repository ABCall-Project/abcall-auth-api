import unittest
from http import HTTPStatus
from flaskr.app import app
from flaskr.infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from flaskr.infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from builder.AuthBuilder import AuthBuilder
from builder.AuthUserCustomerBuilder import AuthUserCustomerBuilder
from builder.RoleBuilder import RoleBuilder
from flaskr.infrastructure.databases.postgres.db import Session
from flaskr.infrastructure.databases.model_sqlalchemy import RoleModelSqlAlchemy, AuthUserModelSqlAlchemy, AuthUserCustomerModelSqlAlchemy

class AuthUserIntegrationTestCase(unittest.TestCase):
    def delete_data(self):
        with Session() as session:
            session.query(AuthUserCustomerModelSqlAlchemy).delete()
            session.query(AuthUserModelSqlAlchemy).delete()
            session.query(RoleModelSqlAlchemy).delete()
            session.commit()
    def add_role(self, role):
        with Session() as session:
            new_role = RoleModelSqlAlchemy(
                id=role.id,
                name=role.name
            )
            session.add(new_role)
            session.commit()
    
    def add_auth_user(self, auth):
        with Session() as session:
            new_auth = AuthUserModelSqlAlchemy(
                id=auth.id,
                name=auth.name,
                password=auth.password,
                last_name=auth.last_name,
                phone_number=auth.phone_number,
                address=auth.address,
                birthdate=auth.birthdate,
                role_id=auth.role_id,
                salt=auth.salt
            )
            session.add(new_auth)
            session.commit()

    def add_auth_user_customer(self, auth_customer):
        with Session() as session:
            new_auth_customer = AuthUserCustomerModelSqlAlchemy(
                id=auth_customer.id,
                auth_user_id=auth_customer.auth_user_id,
                customer_id=auth_customer.customer_id
            )
            session.add(new_auth_customer)
            session.commit()

    def setUp(self):
        self.auth_repository = AuthPostgresqlRepository()
        self.auth_user_customer_repository = AuthCustomerPostgresqlRepository()
        return super().setUp()
    
    def tearDown(self):
        self.delete_data()
        return super().tearDown()
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    
    def test_should_get_users_by_customer_id(self):
        role = RoleBuilder().build()
        self.add_role(role)
        auth = AuthBuilder().with_role_id(role.id).build()
        auth_customer = AuthUserCustomerBuilder().with_auth_user_id(auth.id).build()
        self.add_auth_user(auth)
        self.add_auth_user_customer(auth_customer)

        response = self.client.get(f'/users/getUsersByCustomer?customer_id={auth_customer.customer_id}', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_should_return_internal_server_error_when_some_error_happen_in_get_users_by_customer_id(self):
        response = self.client.get('/users/getUsersByCustomer?customer_id=123', content_type='application/json')
        
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_should_return_not_found_when_action_not_found(self):
        response = self.client.get('/users/getUsersByTest?customer_id=123', content_type='application/json')
        
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    
    def test_should_get_users_by_role_id(self):
        role = RoleBuilder().build()
        self.add_role(role)
        auth = AuthBuilder().with_role_id(role.id).build()
        self.add_auth_user(auth)

        response = self.client.get(f'/users/getUsersByRole?role_id={role.id}', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_internal_server_error_when_some_error_happen_in_get_users_by_role_id(self):
        response = self.client.get('/users/getUsersByRole?role_id=123', content_type='application/json')
        
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_should_get_company_by_user_id(self):
        role = RoleBuilder().build()
        self.add_role(role)
        auth = AuthBuilder().with_role_id(role.id).build()
        self.add_auth_user(auth)
        auth_customer = AuthUserCustomerBuilder().with_auth_user_id(auth.id).build()
        self.add_auth_user_customer(auth_customer)

        response = self.client.get(f'/users/getCompanyByUser?user_id={auth_customer.auth_user_id}', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_should_return_internal_server_error_when_some_error_happen_in_get_company_by_user_id(self):
        response = self.client.get('/users/getCompanyByUser?user_id=123', content_type='application/json')
        
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
