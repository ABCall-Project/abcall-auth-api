from typing import List, Optional
from uuid import UUID
from ..models.auth import Auth

class AuthRepository:
    def list_users_by_role(self,role_id) -> List[Auth]:
        raise NotImplementedError
    
    def create(self, user: Auth)-> Auth:
        raise NotImplementedError
    
    def get_user_by_credentials(self,email)->Auth:
        raise NotImplementedError