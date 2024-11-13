from typing import List
from flaskr.domain.interfaces import AuthUserCustomerRepository
from flaskr.domain.models import AuthUserCustomer

class AuthCustomerMockRepository(AuthUserCustomerRepository):
    def __init__(self, authUsersMock: list[AuthUserCustomer] = []):
        super().__init__()
        self.auth_users = authUsersMock

    def list_users_by_customer(self, customer_id) -> List[AuthUserCustomer]:
        return [auth_user for auth_user in self.auth_users if auth_user.customer_id == customer_id]

    def get_company_by_user(self, user_id) -> AuthUserCustomer:
        return next((auth_user for auth_user in self.auth_users if auth_user.auth_user_id == user_id), None)

    def create(self, user:AuthUserCustomer) -> AuthUserCustomer:
        self.auth_users.append(user)
        return user
        