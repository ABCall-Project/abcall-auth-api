from datetime import datetime

class Auth:
    def __init__(self, id,name:str,last_name:str,phone_number:str,email:str,address:str,birthdate:datetime,role_id:str):
        self.id=id
        self.name =name
        self.last_name=last_name
        self.phone_number=phone_number
        self.email=email
        self.address=address
        self.birthdate=birthdate
        self.role_id=role_id

    def to_dict(self):
        return {
            'id': str(self.id),
	        "name" : str(self.name),
	        "last_name" : str(self.last_name),
	        "phone_number" : str(self.phone_number),
	        "email" : str(self.email),
	        "address" : str(self.address),
	        "birthdate": self.birthdate.strftime("%Y-%m-%d") if self.birthdate else None,
	        "role_id": str(self.role_id)
        }