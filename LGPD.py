import os
import time
import csv
import logging
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, text

PASTA_SAIDA = 'resultados'
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

logging.basicConfig(
    filename=os.path.join(PASTA_SAIDA, 'tempo_execucao.log'), 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()  
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()     
        duracao = fim - inicio
        logging.info(f"Função '{func.__name__}' executada em {duracao:.6f} segundos.")
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

    created = created.strftime('%Y-%m-%d %H:%M:%S') if created else ''
    updated = updated.strftime('%Y-%m-%d %H:%M:%S') if updated else ''

    
    return (id_val, nome_anon, cpf_anon, email_anon, telefone_anon, dt_nasc, created, updated)



@medir_tempo
def gerar_arquivos_por_ano(users_anonimizados):
    anos = {}
    for user in users_anonimizados:
        ano = user[5].year 
        if ano not in anos:
            anos[ano] = []
        anos[ano].append(user)
        
    for ano, registros in anos.items():
        caminho_arquivo = os.path.join(PASTA_SAIDA, f"{ano}.csv")
        with open(caminho_arquivo, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'created_on', 'updated_on'])
            writer.writerows(registros)

@medir_tempo
def gerar_arquivo_todos(users_originais):
    caminho_arquivo = os.path.join(PASTA_SAIDA, "todos.csv")
    with open(caminho_arquivo, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['nome', 'cpf'])
        for user in users_originais:
            writer.writerow([user[1], user[2]]) 

if __name__ == "__main__":
    users_originais = []
    users_anonimizados = []

    print(f"Processando registros e salvando em '{PASTA_SAIDA}'...")
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios;"))
        for row in result:
            linha_tupla = tuple(row)
            users_originais.append(linha_tupla)
            users_anonimizados.append(LGPD(linha_tupla))

    gerar_arquivos_por_ano(users_anonimizados)
    gerar_arquivo_todos(users_originais)

    print(f" Concluído! Todos os arquivos estão na pasta '{PASTA_SAIDA}'.")