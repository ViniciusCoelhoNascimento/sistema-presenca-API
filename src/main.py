from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Aulas, Professores, Turmas
import schemas
import auth

# Importa os modelos para que o SQLAlchemy os conheça
from models import Base

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register(professor: schemas.ProfessorCreate, db: Session = Depends(get_db)):

    #Verifica se o usuário já existe
    existing_user = db.query(Professores).filter(professor.username == Professores.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Autor já existe")

    #Gerando o hash da senha do author
    hashed_password = auth.hash_password(professor.password)

    #Cria novo autor
    db_profesor = Professores(username=professor.username,
        email = professor.email, password=hashed_password)
    db.add(db_profesor)
    db.commit()

    #Cria o token JWT para o usuário recém criado
    token = auth.create_token({"sub": professor.username},
                expires_delta=auth.timedelta(hours=2))
    
    return {"msg": "Usuário registrado com sucesso", "access_token": token}

@app.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Professores).filter(Professores.username == user.username).first()

    if not db_user or not auth.verify_password(user.password,
                                db_user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
        #Cria o token JWT para o usuário recém criado
    token = auth.create_token({"sub": db_user.username},
                expires_delta=auth.timedelta(hours=2))
    return {"acess_token": token}

@app.post("/create-aula/")
def create_post(
    aula: schemas.CreateAula,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user)  # Obtém o usuário autenticado
):
    db_user = db.query(Professores).filter(Professores.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Cria a nova aula
    db_aula = models.Aulas(
        descricao=aula.descricao,
        id_professor=aula.id_professor
    )
    
    db.add(db_aula)
    db.commit()
    db.refresh(db_aula)
    
    # return db_aula
    return {"msg": "Aula criado com sucesso"}

@app.post("/create-turma/")
def create_post(
    turma: schemas.CreateTurma,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user)  # Obtém o usuário autenticado
):
    db_user = db.query(Professores).filter(Professores.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db_turma = models.Turmas(
        descricao=turma.nome_aluno,
        presenca=turma.presenca,
        id_professor=turma.id_aula
    )
    
    db.add(db_turma)
    db.commit()
    db.refresh(db_turma)
    
    # return db_aula
    return {"msg": "Turma criado com sucesso"}

@app.put("/check-presenca/")
def update_presenca(
    presenca: schemas.UpdatePresenca,
    db: Session = Depends(get_db),
    username: str = Depends(auth.get_current_user)  # Obtém o usuário autenticado
):
    db_user = db.query(Professores).filter(Professores.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Busca o registro de presença do aluno
    db_turma = db.query(Turmas).filter(
        Turmas.nome_aluno == presenca.nome_aluno,
        Turmas.id_aula == presenca.id_aula
    ).first()
    

    # Se não existir, retorna erro
    if not db_turma:
        raise HTTPException(
            status_code=404,
            detail=f"Aluno {presenca.nome_aluno} não encontrado na aula"
        )

     # Atualiza o status de presença
    db_turma.presenca = presenca.presenca

    db.commit()
    db.refresh(db_turma)
    
    # return db_aula
    return {"msg": "Presenca alterada com sucesso"}

@app.get("/aulas/")
def get_all_aulas(db: Session = Depends(get_db)):
    aulas = db.query(Aulas).all()
    return aulas

@app.get("/alunos/")
def get_alunos_aula(
    id_aula: int,  # Parâmetro de consulta para filtrar por id_aula
    db: Session = Depends(get_db)
):
    # Filtra os alunos pelo id_aula fornecido
    alunos = db.query(Turmas).filter(
        Turmas.id_aula == id_aula
    ).all()

    return alunos