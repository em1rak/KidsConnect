import hashlib
import secrets
import hmac

def hash_password(password: str) -> str:
    """Хэширование пароля с использованием PBKDF2 HMAC SHA256 и солью."""
    salt = secrets.token_bytes(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{salt.hex()}${hash_bytes.hex()}"

def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Проверка соответствия открытого пароля хэшу."""
    try:
        salt_hex, hash_hex = stored_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        calculated_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return hmac.compare_digest(calculated_hash, expected_hash)
    except Exception:
        return False

def generate_token() -> str:
    """Генерация случайного криптографически стойкого токена авторизации."""
    return secrets.token_urlsafe(32)
