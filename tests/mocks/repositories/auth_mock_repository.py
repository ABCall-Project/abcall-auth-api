from typing import List
from flaskr.domain.interfaces import AuthRepository
from flaskr.domain.models import Auth


class AuthMockRepository(AuthRepository):
    def __init__(self, userMock: list[Auth] = []):
        super().__init__()
        self.users = userMock

    def list_users_by_role(self, role_id):
        return [user for user in self.users if user.role_id == role_id]

    def create(self, user:Auth) -> Auth:
        self.users.append(user)
        return user

    def find_by_email(self, email:str) -> Auth:
        return next((user for user in self.users if user.email == email), None)