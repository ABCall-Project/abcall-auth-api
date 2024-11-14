from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from http import HTTPStatus
from ...application.auth_service import AuthService
from ...infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from ...infrastructure.databases.auth_postresql_repository import AuthPostgresqlRepository
from ...utils import Logger

from config import Config

log = Logger()

class AuthUser(Resource):

    def __init__(self):
        config = Config()
        self.auth_user_customer_repository = AuthCustomerPostgresqlRepository(config.DATABASE_URI)
        self.auth_repository = AuthPostgresqlRepository(config.DATABASE_URI)
        self.service = AuthService(self.auth_repository, self.auth_user_customer_repository)


    def get(self, action=None):
        if action == 'getUsersByCustomer':
            return self.getUsersByCustomer()
        elif action == 'getUsersByRole':
            return self.getUsersByRole()
        elif action =='getCompanyByUser':
            return self.getCompanyByUser()
        else:
            return {"message": "Action not found"}, 404
        
    def post(self, action=None):
        if action == 'getUserByCredentials':
            return self.get_user_by_credentials()
        else:
            return {"message": "Action not found"}, 404
        
    
    def getUsersByCustomer(self):

        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request to get users by customer {customer_id}')
            user_list = self.service.list_users_by_customer(customer_id)
            list_user = [users.to_dict() for users in user_list]
            
            return list_user, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get the data from {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get rate by customer data'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def getUsersByRole(self):

        try:
            role_id = request.args.get('role_id')
            log.info(f'Receive request to get users by role {role_id}')
            user_list = self.service.list_users_by_role(role_id)
            list_user = [users.to_dict() for users in user_list]
            
            return list_user, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get the data from {role_id}: {ex}')
            return {'message': 'Something was wrong trying to get rate by role data'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    
    def getCompanyByUser(self):
        try:
            user_id = request.args.get('user_id')
            log.info(f'Receive request to get company by user {user_id}')
            user_company = self.service.get_company_by_user(user_id)
            if user_company:
                user_company_s=user_company.to_dict()
                return user_company_s, HTTPStatus.OK
            else:
                return None, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get the data company by user: {ex}')
            return {'message': 'Something was wrong trying to get data company by user'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    def get_user_by_credentials(self):
        try:

            if request.is_json:  
                data = request.get_json()
                email = data.get('email')
                password = data.get('password')
                log.info(f'Receive request to get user by credentials {email}')
                user = self.service.get_user_by_credentials(email,password)
                company=None
                user_company = self.service.get_company_by_user(user.id)
                    
                if user and user_company:
                    #quering company by user
                    company=user_company.customer_id

                    return {
                        "id": str(user.id),
                        "name": user.name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "email": user.email,
                        "address": user.address,
                        "birthdate": user.birthdate.strftime("%Y-%m-%d") if user.birthdate else None,
                        "role_id": str(user.role_id),
                        "customer_id":str(company)
                    }, HTTPStatus.OK
                else:
                    return None, HTTPStatus.NOT_FOUND
            else:
                return None, HTTPStatus.BAD_REQUEST
        
            
        except Exception as ex:
            log.error(f'Some error occurred trying to get user by credentials: {ex}')
            return {'message': 'Something was wrong trying to get user by credentials'}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    