from sqlalchemy.ext.asyncio import AsyncSession
from models import Vehiculo

async def crear(db: AsyncSession):
    vehiculo = Vehiculo()
    db.add(vehiculo)
    await db.commit()
    await db.refresh(vehiculo)
    return vehiculo

async def obtener_por_id(db: AsyncSession, vehiculo_id: int):
    return await db.get(Vehiculo, vehiculo_id)