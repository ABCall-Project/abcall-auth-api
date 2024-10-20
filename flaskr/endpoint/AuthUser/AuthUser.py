from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from ...application.auth_service import AuthService
from ...infrastructure.databases.auth_users_customer_postgresql_repository import AuthCustomerPostgresqlRepository
from http import HTTPStatus
from ...utils import Logger

from config import Config

log = Logger()

class AuthUser(Resource):

    def __init__(self):
        config = Config()
        self.auth_user_customer_repository = AuthCustomerPostgresqlRepository(config.DATABASE_URI)
        self.service = AuthService(None,self.auth_user_customer_repository)


    def get(self, action=None):
        if action == 'getUsersByCustomer':
            return self.getUsersByCustomer()
       
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
        
    
    