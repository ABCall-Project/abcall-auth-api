from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import AuthUserCustomer
from ...domain.interfaces import AuthUserCustomerRepository
from ...infrastructure.databases.model_sqlalchemy import Base, AuthUserCustomerModelSqlAlchemy


class AuthCustomerPostgresqlRepository(AuthUserCustomerRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_users_by_customer(self,customer_id) -> List[AuthUserCustomer]:
        session = self.Session()
        try:
            auth_users_customer = session.query(AuthUserCustomerModelSqlAlchemy).filter_by(customer_id=customer_id).all()
            return [self._from_model(auth_user_customer_model) for auth_user_customer_model in auth_users_customer]
        finally:
            session.close()

    
    def _from_model(self, model: AuthUserCustomerModelSqlAlchemy) -> AuthUserCustomer:
        return AuthUserCustomer(
            id=model.id,
            auth_user_id=model.auth_user_id,
            customer_id=model.customer_id
        )