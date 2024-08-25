from flask import  Blueprint, request, jsonify
from myApp.service.usuarioService import get_usuarios, set_usuario, get_usuario_by_id, delete_usuario_by_id, update_usuario

bp = Blueprint("usuarioRoute", __name__)

@bp.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    """Gerencia os usuários com base no método HTTP."""
    if request.method == 'GET':
        return get_usuarios()
    elif request.method == 'POST':
        data = request.json
        return jsonify(set_usuario(data)), 201


@bp.route("/usuarios/<int:id>", methods=['GET', 'DELETE', 'PUT'])
def usuario(id):
    """Gerencia um usuário específico com base no método HTTP e ID."""
    if request.method == 'GET':
        usuario = get_usuario_by_id(id)
        if usuario is not None:
            return jsonify(usuario), 200
        else:
            return jsonify({"error": "Não foi possivel encontrar o usuário informado!"}), 404
    elif request.method == 'PUT':
        data = request.json
        rowUpdate = update_usuario(id, data)
        if rowUpdate > 0:
            return jsonify(data), 201
        else:
            return jsonify({"Error": "Não foi possivel alterar o usuário informado!"}), 304
    elif request.method == 'DELETE':
        rowDelete = delete_usuario_by_id(id)
        if rowDelete > 0:
            return jsonify({"message": "Usuário deletado!"}), 200
        else:
            return jsonify({"Error": "Nãoi foi possivel deletar o usuário informado!"}), 304
        
