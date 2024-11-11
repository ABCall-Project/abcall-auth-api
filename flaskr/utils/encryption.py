from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import os

def generate_key_from_phrase(phrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(phrase.encode()))
    return key

def encrypt_data(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

def validate_cipher(encrypted_data: str, original_data: str, key: bytes) -> bool:
    try:
        decrypted_data = decrypt_data(encrypted_data, key)
        return decrypted_data == original_data
    except Exception as ex:
        return False
    
def base64_encode(data:bytes):
    return base64.b64encode(data).decode('ascii')

def base64_decode(data:str):
    return base64.b64decode(data.encode("ascii"))