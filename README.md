# Estacionamiento API

## Setup

```bash
git clone https://github.com/juanmacevedo/estacionamiento.git
cd estacionamiento
python -m venv venv

venv\Scripts\activate (windows)
source venv/bin/activate (linux)
pip install -r requirements.txt
```

## Base de datos

Instalar postgressql:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Crear DB:
```bash
psql -U postgres
sudo -u postgres psql -U postgres (si no funciona el anterior)

CREATE DATABASE estacionamiento;
\q
```

Crear `.env` en la raíz:
```
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '1234';"
echo -e "DATABASE_URL=postgresql+asyncpg://postgres:1234@localhost:5432/estacionamiento\nDATABASE_URL_SYNC=postgresql+psycopg2://postgres:1234@localhost:5432/estacionamiento" > .env
```

## Migraciones

```bash
alembic upgrade head
```

## Arrancar

```bash
uvicorn main:app --reload
```
