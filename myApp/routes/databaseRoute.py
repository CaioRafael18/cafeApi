from flask import Blueprint, jsonify, current_app

bp = Blueprint('databaseRoute', __name__)

@bp.route('/iniciar', methods=['GET'])
def init_db():
    """Cria e inicia o banco de dados baseado no schema."""
    with current_app.app_context():
        db = current_app.extensions.get('database')
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().execute(f.read())
        db.commit()
    return jsonify({"message": "Banco de dados inicializado com sucesso"}), 200

