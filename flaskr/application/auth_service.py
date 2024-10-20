from typing import List
from ..domain.models import Auth
import requests
from ..domain.interfaces.AuthRepository import AuthRepository
from ..domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
import uuid
from datetime import datetime
from ..utils import Logger
from  config import Config

class AuthService:
    def __init__(self, auth_repository: AuthRepository=None, auth_user_customer_repository: AuthUserCustomerRepository=None):
        self.log = Logger()
        self.auth_repository=auth_repository
        self.auth_user_customer_repository=auth_user_customer_repository

    def list_users_by_customer(self,customer_id):
        return self.auth_user_customer_repository.list_users_by_customer(customer_id)

    