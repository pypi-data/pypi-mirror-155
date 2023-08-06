from base64 import urlsafe_b64decode as b64dec
from base64 import urlsafe_b64encode as b64enc
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import random
import secrets
import os
import logging

logger = logging.getLogger('loz')

kdf_min_iter=200_000
kdf_max_iter=300_000

def _keygen(password: bytes, salt: bytes, iterations: int) -> bytes:
    """Generate secret key using password, salt and iterations."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend())
    return b64enc(kdf.derive(password))

def enc(msg: bytes, password: str) -> bytes:
    """Encrypt message with password."""
    iterations = random.randint(kdf_min_iter, kdf_max_iter)
    salt = secrets.token_bytes(32)
    key = _keygen(password.encode(), salt, iterations)
    logger.debug(f"encrypting secret with {str(iterations)} iterations")
    return b64enc(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64dec(Fernet(key).encrypt(msg)),
        )
    ).decode("utf-8") 

def dec(token: bytes, password: str) -> bytes:
    decoded = b64dec(token)
    salt, iter, token = decoded[:32], decoded[32:36], b64enc(decoded[36:])
    iterations = int.from_bytes(iter, 'big')
    key = _keygen(password.encode(), salt, iterations)
    logger.debug(f"decrypting secret with {str(iterations)} iterations")
    return Fernet(key).decrypt(token)
