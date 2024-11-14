from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Auth
from ...domain.interfaces import AuthRepository
from ...infrastructure.databases.model_sqlalchemy import Base, AuthUserModelSqlAlchemy
from ...utils import Logger
from .postgres.db import Session, engine
log = Logger()
class AuthPostgresqlRepository(AuthRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_users_by_role(self,role_id) -> List[Auth]:
        with self.session() as session:
            log.info('Receive request AuthPostgresqlRepository --->')
            try:
                auth_users= session.query(AuthUserModelSqlAlchemy).filter_by(role_id=role_id).all()
                return [self._from_model(auth_user_model) for auth_user_model in auth_users]
            finally:
                session.close()
    
    def create(self, user: Auth)-> Auth:
        with self.session() as session:
            try:
                auth_user = AuthUserModelSqlAlchemy(
                    name=user.name,
                    password= user.password,
                    last_name=user.last_name,
                    phone_number=user.phone_number,
                    email=user.email,
                    address=user.address,
                    birthdate=user.birthdate,
                    role_id=user.role_id,
                    salt = user.salt
                )
                session.add(auth_user)
                session.commit()
                session.refresh(auth_user)
                return self._from_model(auth_user)
            except Exception as ex:
                log.error(f'Some error occurred trying to create user {ex}')
                raise ex
            finally:
                session.close()
    
    def find_by_email(self, email: str) -> Optional[Auth]:
        with self.session() as session:
            try:
                auth_user = session.query(AuthUserModelSqlAlchemy).filter_by(email=email).first()
                if auth_user:
                    return self._from_model(auth_user)
                else:
                    return None
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
            role_id=model.role_id,
            password=model.password,
            salt=model.salt
        )
    

    def get_user_by_credentials(self,email)->Auth:
        """
            get user by user credentials
            Args: 
                email (str): users email
                password (str): users password

            Returns:
                user (Auth): user instance
        """
        log.info(f'quering user by credentials {email}')
        with self.session() as session:
            try:
                user=session.query(AuthUserModelSqlAlchemy).filter_by(email=email).first()
                if user:
                    log.info(f'user found {user}')
                    return self._from_model(user)
                else:
                    return None
            finally:
                session.close()
