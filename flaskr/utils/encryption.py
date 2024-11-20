from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes
import hmac
import hashlib
from hashlib import sha256
import base64
from flaskr.utils import Logger

log = Logger()

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

def hash_password(password: str, phrase: str) -> str:
    phrase_bytes = phrase.encode('utf-8')
    password_bytes = password.encode('utf-8')

    hashed = hmac.new(phrase_bytes, password_bytes, hashlib.sha256)

    return base64.b64encode(hashed.digest()).decode('utf-8')

def verify_hash(password:str, phrase:str, expected_hash: str)->bool:
    computed_hash = hash_password(password, phrase)

    return computed_hash == expected_hash

def encrypt_data(data: str, key: bytes) -> str:
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

def decrypt_data_with_phrase(encrypted_data: str, phrase: str)->str:
    try:
        key = hashlib.sha256(phrase.encode('utf-8')).digest()
        iv_base64, ciphertext_base64 = encrypted_data.split(":")
        iv = base64.b64decode(iv_base64)
        ciphertext = base64.b64decode(ciphertext_base64)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data.decode('utf-8')
    except ValueError as ex:
        log.error(f"Decryption error: {ex}")
        raise ex
    except Exception as ex:
        log.error(f'Some error ocurred trying to decrypt the data {ex}')
        raise ex


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