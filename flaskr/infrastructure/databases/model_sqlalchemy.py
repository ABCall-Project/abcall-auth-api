from sqlalchemy import Column, String, Numeric, DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class AuthUserModelSqlAlchemy(Base):
    __tablename__ = 'auth_user'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class AuthUserCustomerModelSqlAlchemy(Base):
    __tablename__ = 'auth_user_customer'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_user_id = Column(PG_UUID(as_uuid=True),ForeignKey('auth_user.id'))
    customer_id = Column(PG_UUID(as_uuid=True))
    auth_user = relationship("AuthUserModelSqlAlchemy")