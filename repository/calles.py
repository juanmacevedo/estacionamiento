from sqlalchemy.ext.asyncio import AsyncSession
from models import Calle

async def crear(db: AsyncSession):
    calle = Calle()
    db.add(calle)
    await db.commit()
    await db.refresh(calle)
    return calle

async def obtener_por_id(db: AsyncSession, calle_id: int):
    return await db.get(Calle, calle_id)