# Agenda Médica

## Visão geral

A Agenda Médica é uma aplicação web simples criada para demonstrar um fluxo completo de autenticação, consulta e visualização de agendamentos médicos. A solução foi desenvolvida com Python e Flask no backend, React com Vite no frontend, SQLite como banco de dados e Docker para facilitar a execução.

O projeto permite:
- realizar login com e-mail e senha;
- consultar agendamentos médicos em uma tabela;
- buscar registros por paciente, CPF ou médico;
- exibir mensagens claras para cenários como login inválido, ausência de dados e falhas de comunicação.

## Tecnologias utilizadas

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- React
- Vite
- Tabulator
- Docker e Docker Compose

## Estrutura do projeto

- backend: aplicação Flask com rotas de autenticação e agendamentos
- frontend: interface web em React para exibição da agenda
- data: arquivos de persistência do banco SQLite
- docker-compose.yml: configuração para subir backend, frontend e banco com um único comando

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- Docker
- Docker Compose

## Executando com Docker

Na raiz do repositório, execute:

```bash
docker compose up --build
```

Após a inicialização:
- frontend: http://localhost:5173
- backend: http://localhost:5000

## Usuário de teste

O projeto já inclui dados iniciais carregados por seed. Um exemplo de usuário para login é:

- E-mail: dra.ana@hospital.com
- Senha: senha123

## Fluxo de uso

1. Acesse a tela de login no frontend.
2. Informe o e-mail e a senha do usuário de teste.
3. Após o login, a aplicação carrega os agendamentos e exibe uma tabela com os dados.
4. Utilize a busca para localizar agendamentos por paciente, CPF ou médico.

## Banco de dados

O projeto utiliza SQLite com persistência local no diretório data. A estrutura inicial é criada automaticamente ao iniciar a aplicação, e os dados de exemplo são carregados via seed.

## Decisões técnicas

- O backend foi organizado em blueprints para separar responsabilidades entre autenticação e agendamentos.
- O frontend utiliza uma tabela interativa para facilitar a visualização e a busca de registros.
- O uso de Docker reduz a complexidade de configuração e permite que o projeto seja executado em ambientes diferentes com maior facilidade.

## Limitações conhecidas

- A autenticação atual é simples e baseada em credenciais armazenadas localmente no banco.
- A aplicação foi pensada como uma solução didática e de demonstração, não como uma plataforma empresarial completa.
- Os dados são fornecidos com base em seed local e podem ser substituídos por uma API externa em versões futuras.

## Observações

O projeto foi desenvolvido com foco em praticidade, organização de código e demonstração de boas práticas básicas em desenvolvimento web com Python, banco de dados SQL, integração HTTP e containerização.
