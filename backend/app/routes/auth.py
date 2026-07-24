import secrets
from flask import Blueprint, jsonify, request
from sqlalchemy import select
from app.database import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

active_sessions = {}

def create_session(user_id: int) -> str:
    token = secrets.token_urlsafe(24)
    active_sessions[token] = user_id
    return token


def get_current_user_id() -> int | None:
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ', 1)[1].strip()
    return active_sessions.get(token)

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json() or {}
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not email or not senha:
        return jsonify({"message": "E-mail e senha são obrigatórios"}), 400
    
    query = select(Usuario).where(Usuario.email == email)
    usuario = db.session.execute(query).scalar_one_or_none()
    
    if not usuario or usuario.senha != senha:
        return jsonify({"message": "Usuário ou senha inválidos"}), 401
    
    token = create_session(usuario.id)

    return jsonify({
        "id": usuario.id,
        "email": usuario.email,
        "tipo": usuario.tipo.value,
        "token": token,
    }), 200
    
    
@auth_bp.route('/', methods=['GET'])
def get_all_users():
    query = select(Usuario)
    usuarios = db.session.execute(query).scalars().all()
    
    resultado = [
        {
            "id": a.id,
            "nome": a.nome,
            "email": a.email,
            "senha": a.senha,
            "cpf": a.cpf,
            "tipo": a.tipo.value if a.tipo else None,
            "convenio": a.convenio,
            "especialidade": a.especialidade
        }
        for a in usuarios
    ]
    return jsonify(resultado), 200
