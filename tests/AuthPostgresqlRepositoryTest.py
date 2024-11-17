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

    # def test_list_users_by_role(self):
    #     sample_role_id = "admin"
    #     sample_page = 1
    #     sample_limit = 10  # mock limit, it must be a valid integer to avoid division by None

    #     # Create a mock user to return in the query
    #     mock_user = AuthUserModelSqlAlchemy(
    #         id=uuid4(),
    #         name="John",
    #         last_name="Doe",
    #         phone_number="1234567890",
    #         email="john.doe@example.com",
    #         address="123 Main St",
    #         birthdate=datetime(1990, 1, 1),
    #         role_id=sample_role_id
    #     )

    #     # Mock the session query and count
    #     mock_session = self.mock_session_instance
    #     mock_session.query.return_value.filter.return_value.filter_by.return_value.count.return_value = 5  # mock total items (e.g., 5 users)
        
    #     # Mock query to return a list of users
    #     mock_session.query.return_value.filter_by.return_value.all.return_value = [mock_user]
        
    #     # Call the method under test
    #     result = self.repo.list_users_by_role(sample_role_id, page=sample_page, limit=sample_limit)

    #     # Assertions
    #     self.assertEqual(len(result["data"]), 1)  # One user returned in the list
    #     self.assertEqual(result["data"][0]["role_id"], sample_role_id)  # The role_id matches
    #     self.assertEqual(result["total_pages"], 1)  # With 5 users and a limit of 10, total pages should be 1
    #     self.assertEqual(result["has_next"], False)  # No next page since total pages is 1

    #     # Check if the session's query methods were called as expected
    #     mock_session.query.assert_called_once_with(AuthUserModelSqlAlchemy)
    #     mock_session.query().filter.assert_called_once_with(AuthUserModelSqlAlchemy.role_id == sample_role_id)
    #     mock_session.query().filter().count.assert_called_once()  # Verify count was called to get total_items
    #     mock_session.query().filter().all.assert_called_once()  # Verify all() was called to get the list of users


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

