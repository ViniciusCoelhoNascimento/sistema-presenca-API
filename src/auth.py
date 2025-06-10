import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import HTTPException, Header

SECRET_KEY = "meu_top_secret"
ALGORITHM = "HS256"

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Retorna os dados decodificados do token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado, faça login novamente")  #  Mensagem mais clara
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token JWT não fornecido corretamente")
    
    token = authorization.split(" ")[1]  # Obtém o token JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Verifica o token
        return payload.get("sub")  # 🔹 Retorna o usuário autenticado
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado, faça login novamente")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
