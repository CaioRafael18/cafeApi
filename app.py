from flask import Flask, g
from myApp.routes.usuarioRoute import bp as usuarioRoute_bp
from myApp.routes.databaseRoute import bp as databaseRoute_bp

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    """Encerra a conexão após a solicitação."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.register_blueprint(usuarioRoute_bp)
app.register_blueprint(databaseRoute_bp)

if __name__ == "__main__":
    app.run(debug=True)
