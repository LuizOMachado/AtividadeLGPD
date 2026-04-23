# Segundo Mini Projeto - Anonimização de Dados (LGPD)

Este repositório contém a solução do Segundo Mini Projeto da Fatec Rio Claro. O sistema foi desenvolvido em Python e tem como objetivo extrair registros de um banco de dados PostgreSQL, aplicar regras de mascaramento em dados sensíveis conforme as diretrizes da Lei Geral de Proteção de Dados (Lei nº 13.709/2018) e exportar relatórios formatados.

## Funcionalidades Implementadas

O script atende aos quatro requisitos do projeto:
* **Atividade 1:** Mascaramento de dados pessoais sensíveis, incluindo Nome, CPF, E-mail e Telefone, utilizando manipulação de strings.
* **Atividade 2:** Geração de relatórios (arquivos `.csv`) separando os usuários anonimizados de acordo com o ano de nascimento.
* **Atividade 3:** Exportação de um arquivo único (`todos.csv`) contendo apenas os dados brutos (não anonimizados) de Nome e CPF.
* **Atividade 4:** Utilização de decoradores (`@wraps`) e da biblioteca `logging` para mensurar e salvar o tempo de execução dos relatórios em um arquivo de log local.

## Tecnologias e Bibliotecas

* Python 3.x
* SQLAlchemy (Conexão e manipulação do banco de dados)
* psycopg2-binary (Driver para PostgreSQL)
* python-dotenv (Gerenciamento seguro de credenciais)

## Configuração do Ambiente

Clone o repositório para a sua máquina local.
* git clone https://github.com/LuizOMachado/AtividadeLGPD

Instale as dependências do projeto executando o comando abaixo no terminal:
*  pip install -r requirements.txt
