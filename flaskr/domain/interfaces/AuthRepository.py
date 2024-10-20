from typing import List, Optional
from uuid import UUID
from ..models.auth import Auth

class AuthRepository:
    def list(self) -> List[Auth]:
        raise NotImplementedError