from pydantic import BaseModel, EmailStr
import datetime

class ProfessorCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class CreateAula(BaseModel):
    descricao: str
    id_professor: int

class CreateTurma(BaseModel):
    nome_aluno: str
    presenca: bool
    id_aula: int

class UpdatePresenca(BaseModel):
    id_aula: int
    nome_aluno: str
    presenca: bool