import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from uuid import uuid4
from datetime import datetime
from flaskr.infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from flaskr.domain.models import Auth
from flaskr.infrastructure.databases.model_sqlalchemy import AuthUserModelSqlAlchemy

class TestAuthPostgresqlRepository(unittest.TestCase):

    @patch('flaskr.infrastructure.databases.auth_postresql_repository.engine')
    @patch('flaskr.infrastructure.databases.auth_postresql_repository.Session')
    def setUp(self, mock_session, mock_engine):
        mock_engine.return_value = mock_engine

        self.mock_session_instance = mock_session.return_value.__enter__.return_value

        self.repo = AuthPostgresqlRepository()

    def test_get_user_by_credentials_found(self):
        email = "john.doe@example.com"
        mock_user = AuthUserModelSqlAlchemy(
            id=uuid4(),
            name="John",
            last_name="Doe",
            phone_number="1234567890",
            email=email,
            address="123 Main St",
            birthdate=datetime(1990, 1, 1),
            role_id="admin",
            password="hashed_password"
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = mock_user

        result = self.repo.get_user_by_credentials(email)

        self.assertIsNotNone(result)
        self.assertEqual(result.email, email)
        self.assertEqual(result.name, "John")
        self.mock_session_instance.query.assert_called_once_with(AuthUserModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(email=email)

    def test_get_user_by_credentials_not_found(self):
        email = "non.existing@example.com"
        self.mock_session_instance.query.return_value.filter_by.return_value.first.return_value = None

        result = self.repo.get_user_by_credentials(email)

        self.assertIsNone(result)
        self.mock_session_instance.query.assert_called_once_with(AuthUserModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(email=email)

