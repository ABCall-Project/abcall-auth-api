from flask_restful import Resource
from flask import jsonify, request
from flask.views import MethodView
import os
import logging
import requests
from http import HTTPStatus
from ...application.auth_service import AuthService
from ...infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from ...infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from ...utils import Logger
from .validation_user import validate_user
from flaskr.utils.encryption import generate_key_from_phrase, encrypt_data, base64_encode
from flaskr.domain.models import Auth

from config import Config

log = Logger()

class User(MethodView):

    def __init__(self):
        self.auth_user_customer_repository = AuthCustomerPostgresqlRepository()
        self.auth_repository = AuthPostgresqlRepository()
        self.service = AuthService(self.auth_repository, self.auth_user_customer_repository)
        self.config = Config()
    @validate_user()
    def post(self):

        try:
            name = request.form.get('name')
            last_name = request.form.get('last_name')
            phone_number = request.form.get('phone_number')
            email = request.form.get('email')
            address = request.form.get('address')
            birthdate = request.form.get('birthdate')
            role_id = request.form.get('role_id')
            customer_id = request.form.get('customer_id')
            password = request.form.get('password')

            salt = os.urandom(16)
            key = generate_key_from_phrase(self.config.PHRASE_KEY, salt)
            password_encrypted = encrypt_data(password, key)

            user = Auth(
                id = None,
                name=name,
                password=password_encrypted,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                address=address,
                birthdate=birthdate,
                role_id=role_id,
                salt=base64_encode(salt),
            )
            
            self.service.post_user_company(user, customer_id)

            return {
                "message": "User created successfully"
            }, HTTPStatus.OK
        except ValueError as ex:
            if (ex.message == 'User already exists'):
                return {'message': 'User already exists'}, HTTPStatus.CONFLICT
        except Exception as ex:
            log.error(f'Some error ocurred trying to save the data: {ex}')
            return {'message': 'Some error ocurred trying to save the data:'}, HTTPStatus.INTERNAL_SERVER_ERROR
    