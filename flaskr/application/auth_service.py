from typing import List
from ..domain.models import Auth
from ..domain.interfaces.AuthRepository import AuthRepository
from ..domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
from ..utils import Logger

class AuthService:
    def __init__(self, auth_repository: AuthRepository=None, auth_user_customer_repository: AuthUserCustomerRepository=None):
        self.log = Logger()
        self.auth_repository=auth_repository
        self.auth_user_customer_repository=auth_user_customer_repository

    def list_users_by_customer(self,customer_id):
        return self.auth_user_customer_repository.list_users_by_customer(customer_id)

    def list_users_by_role(self,role_id):
        self.log.info('Receive AuthService list_users_by_role')
        return self.auth_repository.list_users_by_role(role_id)
    

    def get_company_by_user(self,user_id):
         self.log.info('returning  company by user id')
         return self.auth_user_customer_repository.get_company_by_user(user_id)

    