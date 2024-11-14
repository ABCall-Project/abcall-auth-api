import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, request, jsonify
from http import HTTPStatus
from flaskr.endpoint.AuthUser.AuthUser import AuthUser
from flaskr.application.auth_service import AuthService
from flaskr.app import app

class TestAuthUserView(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.testing = True


    def test_should_return_not_found_when_the_get_path_does_not_exist(self):
      
        error_message = "Action not found"

        response = self.client.get('/auth_user/getFakePath', content_type='multipart/form-data', data=None)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @patch.object(AuthService, 'list_users_by_customer')
    def test_get_users_by_customer_success(self, mock_list_users_by_customer):
        mock_list_users_by_customer.return_value = [
            MagicMock(to_dict=lambda: {"id": "1", "name": "User1"}),
        ]
        auth_user_view = AuthUser()

        with app.test_request_context('/auth_user?action=getUsersByCustomer', method='GET', query_string={'customer_id': '1'}):
            response = auth_user_view.get(action='getUsersByCustomer')
            self.assertEqual(response[1], HTTPStatus.OK)

    # @patch.object(AuthService, 'list_users_by_role')
    # def test_get_users_by_role_success(self, mock_list_users_by_role):
    #     mock_list_users_by_role.return_value = [
    #         MagicMock(to_dict=lambda: {"id": "1", "name": "User1"}),
    #         MagicMock(to_dict=lambda: {"id": "2", "name": "User2"})
    #     ]

    #     with self.app.test_request_context('/auth_user?action=getUsersByRole', method='GET', query_string={'role_id': 'admin'}):
    #         response = self.auth_user_view.get(action='getUsersByRole')
    #         self.assertEqual(response[1], HTTPStatus.OK)
    #         self.assertEqual(len(response[0]), 2)
    #         self.assertEqual(response[0][0]['name'], 'User1')

    # @patch.object(AuthService, 'get_company_by_user')
    # def test_get_company_by_user_success(self, mock_get_company_by_user):
    #     mock_get_company_by_user.return_value = MagicMock(to_dict=lambda: {"customer_id": "123"})

    #     with self.app.test_request_context('/auth_user?action=getCompanyByUser', method='GET', query_string={'user_id': '1'}):
    #         response = self.auth_user_view.get(action='getCompanyByUser')
    #         self.assertEqual(response[1], HTTPStatus.OK)
    #         self.assertEqual(response[0]['customer_id'], '123')


  

    # @patch.object(AuthService, 'get_user_by_credentials')
    # @patch.object(AuthService, 'get_company_by_user')
    # def test_post_get_user_by_credentials_success(self, mock_get_company_by_user, mock_get_user_by_credentials):
    #     mock_get_user_by_credentials.return_value = MagicMock(
    #         id="1", name="John", last_name="Doe", phone_number="1234567890",
    #         email="john.doe@example.com", address="123 Main St",
    #         birthdate=datetime(1990, 1, 1), role_id="admin"
    #     )
    #     mock_get_company_by_user.return_value = MagicMock(customer_id="123")

    #     with self.app.test_request_context('/auth_user?action=getUserByCredentials', method='POST', json={
    #         'email': 'john.doe@example.com', 'password': 'password123'
    #     }):
    #         response = self.auth_user_view.post(action='getUserByCredentials')
    #         self.assertEqual(response[1], HTTPStatus.OK)
    #         self.assertEqual(response[0]['name'], 'John')
    #         self.assertEqual(response[0]['customer_id'], '123')

    # def test_post_get_user_by_credentials_missing_data(self):
    #     with self.app.test_request_context('/auth_user?action=getUserByCredentials', method='POST', json={}):
    #         response = self.auth_user_view.post(action='getUserByCredentials')
    #         self.assertEqual(response[1], HTTPStatus.BAD_REQUEST)

    # @patch.object(AuthService, 'get_user_by_credentials')
    # def test_post_get_user_by_credentials_user_not_found(self, mock_get_user_by_credentials):
    #     mock_get_user_by_credentials.return_value = None

    #     with self.app.test_request_context('/auth_user?action=getUserByCredentials', method='POST', json={
    #         'email': 'nonexistent@example.com', 'password': 'wrongpassword'
    #     }):
    #         response = self.auth_user_view.post(action='getUserByCredentials')
    #         self.assertEqual(response[1], HTTPStatus.NOT_FOUND)
