class Role:
    def __init__(self, id, name: str,):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            'id': str(self.id),
            "name": str(self.name),
        }
