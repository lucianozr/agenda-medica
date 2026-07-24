import os
from flask import Flask
from app.database import db
from app.routes.auth import auth_bp
from app.routes.schedule import schedule_bp

def create_app():
    # Cria a instância da aplicação Flask
    flask_app = Flask(__name__)  # Renomeamos para flask_app para evitar qualquer ambiguidade de escopo

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    local_db_path = os.path.join(data_dir, 'dev.db')

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{local_db_path}')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(flask_app)

    with flask_app.app_context():
        from app.models import Usuario, Agendamento
        db.create_all()

    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(schedule_bp)

    return flask_app