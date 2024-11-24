from uuid import UUID
from flaskr.domain.models import Role

class RoleBuilder:
    def __init__(self):
        self.id = UUID('a257ee3b-c1c6-4139-84bc-f70595a1c780')
        self.name = "admin"
        

    def with_id(self, id: UUID):
        self.id = id
        return self

    def with_name(self, name):
        self.name = name
        return self

    def build(self):
        return Role(id=self.id, name=self.name)