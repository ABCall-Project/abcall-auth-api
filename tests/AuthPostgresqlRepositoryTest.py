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

    @patch('flaskr.infrastructure.databases.auth_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.auth_postresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        self.mock_engine = MagicMock()
        mock_create_engine.return_value = self.mock_engine

        self.mock_session = MagicMock()
        self.mock_session_instance = MagicMock()
        self.mock_session.return_value = self.mock_session_instance
        mock_sessionmaker.return_value = self.mock_session

        self.repo = AuthPostgresqlRepository('mock_connection_string')
        self.repo.Session = self.mock_session

    def test_list_users_by_role(self):
        sample_role_id = "admin"
        mock_user = AuthUserModelSqlAlchemy(
            id=uuid4(),
            name="John",
            last_name="Doe",
            phone_number="1234567890",
            email="john.doe@example.com",
            address="123 Main St",
            birthdate=datetime(1990, 1, 1),
            role_id=sample_role_id
        )
        self.mock_session_instance.query.return_value.filter_by.return_value.all.return_value = [mock_user]

        result = self.repo.list_users_by_role(sample_role_id)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].role_id, sample_role_id)
        self.mock_session_instance.query.assert_called_once_with(AuthUserModelSqlAlchemy)
        self.mock_session_instance.query().filter_by.assert_called_once_with(role_id=sample_role_id)
