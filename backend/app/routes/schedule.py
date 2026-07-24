from flask import Blueprint, jsonify, request
from sqlalchemy import select, or_
from app.database import db
from app.models import Agendamento, Usuario
from app.routes.auth import get_current_user_id

schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/v1/schedule')

# 1. Rota para Listar Todos
@schedule_bp.route('/', methods=['GET'])
def get_all_schedules():
    if not get_current_user_id():
        return jsonify({"message": "Usuário não autenticado"}), 401

    query = select(Agendamento)
    agendamentos = db.session.execute(query).scalars().all()
    
    resultado = [
        {
            "id": a.id,
            "status": a.status,
            "data_hora": a.data_hora.isoformat() if a.data_hora else None,
            "medico": {
                "nome": a.medico.nome if a.medico else None,
                "email": a.medico.email if a.medico else None,
                "cpf": a.medico.cpf if a.medico else None,
                "tipo": a.medico.tipo.value if a.medico and a.medico.tipo else None,
            },
            "paciente": {
                "nome": a.paciente.nome if a.paciente else None,
                "email": a.paciente.email if a.paciente else None,
                "cpf": a.paciente.cpf if a.paciente else None,
                "tipo": a.paciente.tipo.value if a.paciente and a.paciente.tipo else None,
            },
        }
        for a in agendamentos
    ]
    return jsonify(resultado), 200


@schedule_bp.route('/<string:filtro>', methods=['GET'])
def get_filtered_schedules(filtro):
    if not get_current_user_id():
        return jsonify({"message": "Usuário não autenticado"}), 401

    termo_busca = f"%{filtro}%"

    query = (
        select(Agendamento)
        .where(
            or_(
                Agendamento.status.ilike(termo_busca),
                Agendamento.medico.has(Usuario.cpf.ilike(termo_busca)),
                Agendamento.paciente.has(Usuario.cpf.ilike(termo_busca)),
                Agendamento.medico.has(Usuario.nome.ilike(termo_busca)),
                Agendamento.paciente.has(Usuario.nome.ilike(termo_busca))
        ))
    )

    agendamentos = db.session.execute(query).scalars().all()

    resultado = [
        {
            "id": a.id,
            "status": a.status,
            "data_hora": a.data_hora.isoformat() if a.data_hora else None,
            "medico": {
                "nome": a.medico.nome if a.medico else None,
                "email": a.medico.email if a.medico else None,
                "cpf": a.medico.cpf if a.medico else None,
                "tipo": a.medico.tipo.value if a.medico and a.medico.tipo else None,
            },
            "paciente": {
                "nome": a.paciente.nome if a.paciente else None,
                "email": a.paciente.email if a.paciente else None,
                "cpf": a.paciente.cpf if a.paciente else None,
                "tipo": a.paciente.tipo.value if a.paciente and a.paciente.tipo else None,
            },
        }
        for a in agendamentos
    ]

    return jsonify(resultado), 200