import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = "meu_top_secret"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.now() + expires_delta
    # to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY,
                      algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY,
                            algorithm = ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        print("erro assinatura")
        return None
    except jwt.InvalidTokenError:
        print("erro token inválido")
        return None
    
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
