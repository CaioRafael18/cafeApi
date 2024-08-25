from flask import jsonify
from myApp.database.database import get_db, query_db  

def get_usuarios():
    """Utiliza a função query_db para simplificar a execução de consultas SQL."""
    usuarios = query_db("SELECT * FROM tb_usuario")
    return jsonify([dict(user) for user in usuarios]), 200


def set_usuario(data):
    """Cria um novo usuário e persiste os dados no banco."""
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    query = 'INSERT INTO tb_usuario (nome, nascimento) VALUES (%s, %s) RETURNING id'
    with get_db().cursor() as cursor:
        cursor.execute(query, (nome, nascimento))
        id = cursor.fetchone()[0]
        get_db().commit()
    data['id'] = id
    return data


def get_usuario_by_id(id):
    """Obtém um usuário pelo ID."""
    return query_db("SELECT * FROM tb_usuario WHERE id = %s", [id], one=True)
    

def delete_usuario_by_id(id):
    """Deleta usuário pelo ID"""
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM tb_usuario WHERE id = %s", (id,))
    rowDelete = cursor.rowcount
    get_db().commit()
    cursor.close()
    return rowDelete


def update_usuario(id, data):
    """Atualiza um usuário existente."""
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    query = 'UPDATE tb_usuario SET nome = %s, nascimento = %s WHERE id = %s'
    with get_db().cursor() as cursor:
        cursor.execute(query, (nome, nascimento, id))
        get_db().commit()
    rowUpdate = cursor.rowcount
    return rowUpdate
