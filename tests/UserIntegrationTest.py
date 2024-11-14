import unittest
from flaskr.app import app
from http import HTTPStatus
from faker import Faker
from flaskr.infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from flaskr.infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from flaskr.infrastructure.databases.postgres.db import Session
from flaskr.infrastructure.databases.model_sqlalchemy import RoleModelSqlAlchemy, AuthUserModelSqlAlchemy, AuthUserCustomerModelSqlAlchemy


class UserIntegrationTestCase(unittest.TestCase):
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

    def tearDown(self):
        self.delete_data()
        return super().tearDown()
    
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True

    def test_should_create_user(self):
        fake = Faker()
        role = RoleModelSqlAlchemy(id=fake.uuid4(), name='admin')
        self.add_role(role)
        data = {
            'name': fake.first_name(),
            'last_name': fake.last_name(),
            'phone_number': '0123456789',
            'email': fake.email(),
            'address': fake.address(),
            'birthdate': fake.date_of_birth(),
            'role_id': role.id,
            'customer_id': fake.uuid4(),
            'password': fake.password()
        }

        print(data)

        response = self.client.post('/user', data=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
