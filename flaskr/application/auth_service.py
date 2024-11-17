from flask import jsonify
from typing import List
from uuid import UUID
from ..utils.logger import Logger
from ..domain.models import Auth, AuthUserCustomer
from ..domain.interfaces.AuthRepository import AuthRepository
from ..domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
from flaskr.utils.encryption import base64_decode, generate_key_from_phrase, decrypt_data, decrypt_data_with_passphrase, base64_encode

from config import Config

class AuthService:
    def __init__(self, auth_repository: AuthRepository=None, auth_user_customer_repository: AuthUserCustomerRepository=None):
        self.log = Logger()
        self.config = Config()
        self.auth_repository=auth_repository
        self.auth_user_customer_repository=auth_user_customer_repository

    def list_users_by_customer(self,customer_id):
        return self.auth_user_customer_repository.list_users_by_customer(customer_id)

    def list_users_by_role(self,role_id: UUID,page: int, limit: int):
        self.log.info('Receive AuthService list_users_by_role')
        if not role_id:
            raise ValueError("All fields are required to get an user.")
        return self.auth_repository.list_users_by_role(role_id,page=page,
                    limit=limit)
    
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
       
    def get_user_by_credentials(self,email, password)->Auth:
        self.log.info('returning  user by credentials')
        
        try:
            
            user =self.auth_repository.get_user_by_credentials(email=email)
            self.log.info(f'password and hashed password {password} {user.password}')
            if self.__check_password(password,user):
                return user
            else:
                return None
        except Exception as ex:
            self.log.error(f'Some error occurred trying to get user by credentials {ex}')
            return None
    

    def __check_password(self,password, user):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        salt_decode = base64_decode(user.salt)
        key = generate_key_from_phrase(self.config.PHRASE_KEY, salt_decode)
        password_decode = base64_decode(password)
        password_decrypt = decrypt_data_with_passphrase(password_decode, self.config.PHRASE_KEY)
        password_stored_decrypt = decrypt_data(user.password, key)
        return password_decrypt == password_stored_decrypt
