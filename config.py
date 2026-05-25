from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC", "")

if not DATABASE_URL or not DATABASE_URL_SYNC:
    raise ValueError("DATABASE_URL y DATABASE_URL_SYNC deben estar definidas en el .env")

UNIDAD_TIEMPO = "hours"  # cambiar a "hours" para produccion