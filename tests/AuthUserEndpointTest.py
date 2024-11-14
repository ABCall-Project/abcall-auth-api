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

    @patch.object(AuthUser, '__init__', lambda x: None)  # Mockea el constructor de AuthUser para evitar la conexión a la base de datos
    @patch.object(AuthService, 'list_users_by_customer')
    def test_get_users_by_customer_success(self, mock_list_users_by_customer):
        mock_list_users_by_customer.return_value = [
            MagicMock(to_dict=lambda: {"id": "1", "name": "User1"}),
        ]
        
        
        auth_user_view = AuthUser()
        auth_user_view.service = MagicMock()  

        
        with app.test_request_context('/auth_user/getUsersByCustomer', method='GET', query_string={'customer_id': '1'}):
            response = auth_user_view.get(action='getUsersByCustomer')
            self.assertEqual(response[1], HTTPStatus.OK)

   