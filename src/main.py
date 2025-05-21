from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import auth
import schemas
from models import Author

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register(author: schemas.AuthorCreate, db: Session = Depends(get_db)):

    #Verifica se o usuário já existe
    existing_user = db.query(Author).filter(Author.username == author.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Autor já existe")

    #Gerando o hash da senha do author
    hashed_password = auth.hash_password(author.password)

    #Cria novo autor
    db_author = Author(username=author.username,
        email = author.email, password=hashed_password)
    db.add(db_author)
    db.commit()

    #Cria o token JWT para o usuário recém criado
    token = auth.create_token({"sub": author.username},
                expires_delta=auth.timedelta(hours=2))
    
    return {"msg": "Usuário registrado com sucesso", "access_token": token}