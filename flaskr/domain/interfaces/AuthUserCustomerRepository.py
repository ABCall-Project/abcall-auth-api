from typing import List, Optional
from uuid import UUID
from ..models.auth_user_customer import AuthUserCustomer

class AuthUserCustomerRepository:
    def list_users_by_customer(self,customer_id) -> List[AuthUserCustomer]:
        raise NotImplementedError
    
    def get_company_by_user(self,user_id) -> AuthUserCustomer:
        raise NotImplementedError