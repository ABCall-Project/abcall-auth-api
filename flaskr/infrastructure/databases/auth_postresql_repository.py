from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Auth
from ...domain.interfaces import AuthRepository
from ...infrastructure.databases.model_sqlalchemy import Base, AuthUserModelSqlAlchemy
from ...utils import Logger
log = Logger()
class AuthPostgresqlRepository(AuthRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_users_by_role(self,role_id) -> List[Auth]:
        log.info('Receive request AuthPostgresqlRepository --->')
        session = self.Session()
        try:
            auth_users= session.query(AuthUserModelSqlAlchemy).filter_by(role_id=role_id).all()
            return [self._from_model(auth_user_model) for auth_user_model in auth_users]
        finally:
            session.close()

    def _from_model(self, model: AuthUserModelSqlAlchemy) -> Auth:
        return Auth(
            id=model.id,
            name=model.name,
            last_name=model.last_name,
            phone_number=model.phone_number,
            email=model.email,
            address=model.address,
            birthdate=model.birthdate,
            role_id=model.role_id
        )