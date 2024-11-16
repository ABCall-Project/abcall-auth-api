from functools import wraps
from http import HTTPStatus
import uuid
import re
from flask import request, jsonify
from datetime import datetime

def validate_user():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            name = request.form.get('name')
            last_name = request.form.get('last_name') if request.form.get('last_name') else ''
            phone_number = request.form.get('phone_number') if request.form.get('phone_number') else ''
            email = request.form.get('email')
            address = request.form.get('address') if request.form.get('address') else ''
            birthdate = request.form.get('birthdate') if request.form.get('birthdate') else ''
            password = request.form.get('password')
            role_id = request.form.get('role_id')
            customer_id = request.form.get('customer_id')

            if not name or name == "":
                return jsonify({"message": "Name cannot be empty"}), HTTPStatus.BAD_REQUEST
            
            if not password or password == "":
                return jsonify({"message": "Password cannot be empty"}), HTTPStatus.BAD_REQUEST
            
            if not email or email == "":
                return jsonify({"message": "Email cannot be empty"}), HTTPStatus.BAD_REQUEST
            
            if role_id is None or role_id == "":
                return jsonify({"message": "Role cannot be empty"}), HTTPStatus.BAD_REQUEST
            
            if customer_id is None or customer_id == "":
                return jsonify({"message": "Customner cannot be empty"}), HTTPStatus.BAD_REQUEST
            
            if len(name) > 50:
                return jsonify({"message": "The Name is not complete with the maximum, should be 50 characters"}), HTTPStatus.BAD_REQUEST
            
            if len(last_name) > 50:
                return jsonify({"message": "The Last name is not complete with the maximum, should be 50 characters"}), HTTPStatus.BAD_REQUEST
            
            if len(phone_number) > 10:
                return jsonify({"message": "The phone number is not complete with the maximum, should be 10 characters"}), HTTPStatus.BAD_REQUEST
            
            if len(email) > 100:
                return jsonify({"message": "The email is not complete with the maximum, should be 100 characters"}), HTTPStatus.BAD_REQUEST
            
            if len(address) > 255:
                return jsonify({"message": "The address is not complete with the maximum, should be 255 characters"}), HTTPStatus.BAD_REQUEST
            
            if not re.match(r"[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):
                return jsonify({"message": "The email should be a valid email example@mail.com"}), HTTPStatus.BAD_REQUEST
            
            if birthdate != '' and not validate_date(birthdate):
                return jsonify({"message": "The birthdate should be a date format"}), HTTPStatus.BAD_REQUEST
            
            if not is_valid_uuid(role_id):
                return jsonify({"message": "It is not a valid role id with an uuid format"}), HTTPStatus.BAD_REQUEST

            if not is_valid_uuid(customer_id):
                return jsonify({"message": "It is not a valid customer id with an uuid format"}), HTTPStatus.BAD_REQUEST

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
    
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False