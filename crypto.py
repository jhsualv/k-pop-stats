# crypto.py
from cryptography.fernet import Fernet

from config import ENCRYPTION_KEY

fernet = Fernet(ENCRYPTION_KEY)

def encrypt(value: str) -> str:
    """Encrypt a string and return the encrypted value as a string."""
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    """Decrypt a string and return the decrypted value as a string."""
    return fernet.decrypt(value.encode()).decode()