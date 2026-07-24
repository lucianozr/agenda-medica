import enum
from app.database import db

    
class TipoUsuario(enum.Enum):
    MEDICO = "medico"
    PACIENTE = "paciente"

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(200), nullable=False)
    especialidade = db.Column(db.String(200), nullable=True)
    convenio = db.Column(db.String(200), nullable=True)
    tipo = db.Column(db.Enum(TipoUsuario), nullable=False, default=TipoUsuario.PACIENTE)
    
    
class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    paciente = db.relationship('Usuario', foreign_keys=[paciente_id])
    medico = db.relationship('Usuario', foreign_keys=[medico_id])