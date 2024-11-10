from typing import List
from ..domain.models import Auth
from ..domain.interfaces.AuthRepository import AuthRepository
from ..domain.interfaces.AuthUserCustomerRepository import AuthUserCustomerRepository
from ..utils import Logger

from config import Config
import bcrypt

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
    
    def get_user_by_credentials(self,email, password)->Auth:
        self.log.info('returning  user by credentials')
        
        try:
            
            user =self.auth_repository.get_user_by_credentials(email=email)
            self.log.info(f'password and hashed password {password} {user.password}')
            if self.__check_password(password,user.password):
                return user
            else:
                return None
        except Exception:
            return None
        

    def __hash_password(self,password):
        """
        Genera un hash de la contraseña con una sal aleatoria.
        """

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return hashed_password
    

    def __check_password(self,password, hashed_password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
