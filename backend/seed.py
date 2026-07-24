from datetime import datetime, timedelta
from app import create_app
from app.database import db
from app.models import Usuario, TipoUsuario, Agendamento

def run_seeds():
    app = create_app()

    with app.app_context():
        print("🌱 Iniciando o processo de seeding...")

        db.drop_all()
        db.create_all()

        # 1. Criar Médicos
        medico1 = Usuario(
            nome="Dra. Ana Costa",
            email="dra.ana@hospital.com",
            senha="senha123",
            cpf="111.222.333-44",
            especialidade="Cardiologia",
            tipo=TipoUsuario.MEDICO
        )

        medico2 = Usuario(
            nome="Dr. Carlos Eduardo",
            email="dr.carlos@hospital.com",
            senha="senha123",
            cpf="222.333.444-55",
            especialidade="Pediatria",
            tipo=TipoUsuario.MEDICO
        )

        # 2. Criar Pacientes
        paciente1 = Usuario(
            nome="João da Silva",
            email="joao.silva@email.com",
            senha="senha123",
            cpf="333.444.555-66",
            convenio="Unimed",
            tipo=TipoUsuario.PACIENTE
        )

        paciente2 = Usuario(
            nome="Maria Souza",
            email="maria.souza@email.com",
            senha="senha123",
            cpf="444.555.666-77",
            convenio="Bradesco Saúde",
            tipo=TipoUsuario.PACIENTE
        )

        db.session.add_all([medico1, medico2, paciente1, paciente2])
        db.session.commit()
        print("✅ Usuários (Médicos e Pacientes) inseridos!")

        # 3. Criar Agendamentos
        agendamento1 = Agendamento(
            status="Confirmado",
            data_hora=datetime.now() + timedelta(days=1, hours=2), # Amanhã
            medico_id=medico1.id,
            paciente_id=paciente1.id
        )

        agendamento2 = Agendamento(
            status="Pendente",
            data_hora=datetime.now() + timedelta(days=2, hours=4), # Depois de amanhã
            medico_id=medico2.id,
            paciente_id=paciente2.id
        )

        agendamento3 = Agendamento(
            status="Concluído",
            data_hora=datetime.now() - timedelta(days=3), # 3 dias atrás
            medico_id=medico1.id,
            paciente_id=paciente2.id
        )

        db.session.add_all([agendamento1, agendamento2, agendamento3])
        db.session.commit()
        print("✅ Agendamentos inseridos com sucesso!")

        print("🎉 Seeding finalizado com sucesso!")

if __name__ == '__main__':
    run_seeds()