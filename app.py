import sqlite3
from flask import Flask, request, jsonify, g
from Globals import DATABASE_NAME

app = Flask(__name__)


def get_db():
    """Verifica se a conexão com o banco está em 'g', se não estiver, cria a conexão e armazena em 'g'."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_NAME)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Encerra a conexão após a solicitação."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Função para simplificar a execução de consultas."""
    cursor = get_db().execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def index():
    """Endpoint para retornar a versão atualizada."""
    return jsonify({"versao atualizada": 1}), 200


def get_usuarios():
    """Utiliza a função query_db para simplificar a execução de consultas SQL."""
    usuarios = query_db("SELECT * FROM tb_usuario")
    return jsonify([dict(user) for user in usuarios]), 200


def set_usuario(data):
    """Cria um novo usuário e persiste os dados no banco."""
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    query = 'INSERT INTO tb_usuario (nome, nascimento) VALUES (?, ?)'
    cursor = get_db().cursor()
    cursor.execute(query, (nome, nascimento))
    get_db().commit()
    id = cursor.lastrowid
    data['id'] = id
    cursor.close()
    return data


def get_usuario_by_id(id):
    """Obtém um usuário pelo ID."""
    usuario = query_db("SELECT * FROM tb_usuario WHERE id = ?", [id], one=True)
    if usuario is not None:
        return dict(usuario)
    else:
        return jsonify({"error": "Usuário não encontrado!"}), 404


def update_usuario(id, data):
    """Atualiza um usuário existente."""
    nome = data.get('nome')
    nascimento = data.get('nascimento')
    query = 'UPDATE tb_usuario SET nome = ?, nascimento = ? WHERE id = ?'
    cursor = get_db().cursor()
    cursor.execute(query, (nome, nascimento, id))
    get_db().commit()
    row_update = cursor.rowcount
    cursor.close()
    return row_update


@app.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    """Gerencia os usuários com base no método HTTP."""
    if request.method == 'GET':
        return get_usuarios()
    elif request.method == 'POST':
        data = request.json
        data = set_usuario(data)
        return jsonify(data), 201


@app.route("/usuarios/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(id):
    """Gerencia um usuário específico com base no método HTTP e ID."""
    if request.method == 'GET':
        usuario = get_usuario_by_id(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return {}, 404
    elif request.method == 'PUT':
        data = request.json
        row_update = update_usuario(id, data)
        if row_update:
            return jsonify(data), 201
        else:
            return jsonify({"Error": "Não foi atualizado o usuário"}), 304


def init_db():
    """Cria e inicia o banco de dados baseado no schema."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
