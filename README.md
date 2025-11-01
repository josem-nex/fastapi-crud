# fastapi-crud

cp .env.example .env       # editar .env para actualizar credenciales/puerto


## Docker

docker compose up --build -d

docker compose ps              # ver contenedores y estado
docker compose logs -f web     # ver logs de la app
docker compose logs -f db      # ver logs de Postgres

## No-Docker

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

