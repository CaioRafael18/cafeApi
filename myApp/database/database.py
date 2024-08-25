import psycopg2
from psycopg2.extras import DictCursor
from flask import g
from myApp.config.Globals import DATABASE_NAME, USER_NAME, PASSWORD_NAME

infoConnect = {
    "host": "localhost",
    "database": DATABASE_NAME,
    "user": USER_NAME,
    "password": PASSWORD_NAME
}

def get_db():
    """Verifica se a conexão com o banco está em 'g', se não estiver, cria a conexão e armazena em 'g'."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(**infoConnect)
    return db

def query_db(query, args=(), one=False):
    """Função para simplificar a execução de consultas."""
    conn = get_db()
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute(query, args)
        rv = cursor.fetchall()
        return (rv[0] if rv else None) if one else rv
