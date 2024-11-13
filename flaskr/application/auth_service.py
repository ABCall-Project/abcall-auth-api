from flask import jsonify
from typing import List
from ..utils.logger import Logger
from ..domain.models import Auth, AuthUserCustomer
from ..domain.interfaces.AuthRepository import AuthRepository
from ..domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository

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
    
    def post_user_company(self, user: Auth, customer_id:str):
        try:
            self.log.info('Receive AuthService post_user_company')
            user_found = self.auth_repository.find_by_email(user.email)
            if not user_found:
                new_user = self.auth_repository.create(user)
                new_auth_user_customer = AuthUserCustomer(id=None, auth_user_id=new_user.id, customer_id=customer_id)
                self.auth_user_customer_repository.create(new_auth_user_customer)
                self.log.info('User created')
            else:
                self.log.warn('User already exists')
                raise ValueError('User already exists')
        except Exception as ex:
            self.log.error(f'Some error occurred trying to post user company {ex}')
            raise ex
       

    