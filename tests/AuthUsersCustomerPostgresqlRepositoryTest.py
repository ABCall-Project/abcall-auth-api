import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4

from flaskr.infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from flaskr.domain.models.auth_user_customer import AuthUserCustomer
from flaskr.infrastructure.databases.model_sqlalchemy import AuthUserCustomerModelSqlAlchemy

class TestAuthCustomerPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.auth_users_customer_postgresql_repository.engine')
    @patch('flaskr.infrastructure.databases.auth_users_customer_postgresql_repository.Session')
    def setUp(self, mock_session, mock_engine):
        self.mock_engine = mock_engine
        mock_engine.return_value = self.mock_engine

        self.mock_session_instance = mock_session.return_value.__enter__.return_value

        self.repo = AuthCustomerPostgresqlRepository()

    def test_list_users_by_customer(self):
        sample_customer_id = uuid4()
        mock_user = AuthUserCustomerModelSqlAlchemy(
            id=uuid4(),
            auth_user_id=uuid4(),
            customer_id=sample_customer_id
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.all.return_value = [mock_user]

        result = self.repo.list_users_by_customer(sample_customer_id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].customer_id, sample_customer_id)
        self.mock_session_instance.query.assert_called_once_with(AuthUserCustomerModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(customer_id=sample_customer_id)

    def test_get_company_by_user_found(self):
        sample_user_id = uuid4()
        mock_user = AuthUserCustomerModelSqlAlchemy(
            id=uuid4(),
            auth_user_id=sample_user_id,
            customer_id=uuid4()
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_user

        result = self.repo.get_company_by_user(sample_user_id)

        self.assertIsNotNone(result)
        self.assertEqual(result.auth_user_id, sample_user_id)
        self.mock_session_instance.query.assert_called_once_with(AuthUserCustomerModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(auth_user_id=sample_user_id)

    def test_get_company_by_user_not_found(self):
        sample_user_id = uuid4()
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = None

        result = self.repo.get_company_by_user(sample_user_id)

        self.assertIsNone(result)
        self.mock_session_instance.query.assert_called_once_with(AuthUserCustomerModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(auth_user_id=sample_user_id)

    def test_from_model(self):
        # Prueba del método privado _from_model para asegurar que convierte correctamente
        model_instance = AuthUserCustomerModelSqlAlchemy(
            id=uuid4(),
            auth_user_id=uuid4(),
            customer_id=uuid4()
        )
        result = self.repo._from_model(model_instance)

        self.assertIsInstance(result, AuthUserCustomer)
        self.assertEqual(result.id, model_instance.id)
        self.assertEqual(result.auth_user_id, model_instance.auth_user_id)
        self.assertEqual(result.customer_id, model_instance.customer_id)

    @patch('flaskr.infrastructure.databases.auth_users_customer_postgresql_repository.AuthUserCustomerModelSqlAlchemy')
    def test_list_users_by_customer_exception(self, mock_model):
        # Simula una excepción al listar usuarios por cliente
        self.mock_session_instance.query.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.repo.list_users_by_customer(uuid4())

        self.assertTrue("Database error" in str(context.exception))

    @patch('flaskr.infrastructure.databases.auth_users_customer_postgresql_repository.AuthUserCustomerModelSqlAlchemy')
    def test_get_company_by_user_exception(self, mock_model):
        # Simula una excepción al obtener la compañía por usuario
        self.mock_session_instance.query.side_effect = Exception("Database error")

        with self.assertRaises(Exception) as context:
            self.repo.get_company_by_user(uuid4())

        self.assertTrue("Database error" in str(context.exception))

