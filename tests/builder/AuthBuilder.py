from uuid import UUID
from flaskr.domain.models import Auth


class AuthBuilder:
    def __init__(self):
        self.id = UUID("a257ee3b-c1c6-4139-84bc-f70595a1c773")
        self.name = 'User'
        self.last_name = 'Tester'
        self.phone_number = '123456789'
        self.email = 'test@mail.com'
        self.address = '123 Main St'
        self.birthdate = '1990-01-01'
        self.role_id = UUID("a257ee3b-c1c6-4139-84bc-f70595a1c780")
        self.password = 'password'
        self.salt = None

    def with_id(self, id: UUID):
        self.id = id
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def with_last_name(self, last_name: str):
        self.last_name = last_name
        return self

    def with_phone_number(self, phone_number: str):
        self.phone_number = phone_number
        return self

    def with_email(self, email: str):
        self.email = email
        return self

    def with_address(self, address: str):
        self.address = address
        return self

    def with_birthdate(self, birthdate: str):
        self.birthdate = birthdate
        return self

    def with_role_id(self, role_id: UUID):
        self.role_id = role_id
        return self

    def with_password(self, password: str):
        self.password = password
        return self

    def with_salt(self, salt: str):
        self.salt = salt
        return self

    def build(self):
        return Auth(id=self.id, name=self.name, last_name=self.last_name, phone_number=self.phone_number, email=self.email, address=self.address, birthdate=self.birthdate, role_id=self.role_id, password=self.password, salt=self.salt)
