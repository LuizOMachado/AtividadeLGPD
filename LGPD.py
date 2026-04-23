import os
import time
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text

def medir_tempo(func):
    """Decorator que mede o tempo de execução de uma função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  # tempo inicial (mais preciso que time.time)
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     # tempo final
        duracao = fim - inicio
        print(f"⏱ Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper


load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASS')
DATABASE = os.getenv('DB_NAME')
    
engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}")
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)

@medir_tempo
def LGPD(row):
    id_val, nome, cpf, email, telefone, dt_nasc, created, updated = row
    partes = nome.split(' ', 1)
    primeiro_nome = partes[0]
    nome_anon = primeiro_nome[0] + "*" * (len(primeiro_nome) - 1)
    if len(partes) > 1:
        nome_anon += " " + partes[1]
    cpf_anon = f"{cpf[:4]}*** ***-**"
    usuario, dominio = email.split('@')
    email_anon = f"{usuario[0]}{'*' * (len(usuario) - 1)}@{dominio}"
    telefone_anon = telefone[-4:]

    
    return (id_val, nome_anon, cpf_anon, email_anon, telefone_anon, dt_nasc, created, updated)

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        
        row_anonimizada = LGPD(tuple(row))
        users.append(row_anonimizada)


for user in users:
    print(user)