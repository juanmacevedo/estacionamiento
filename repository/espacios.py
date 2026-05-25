from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from models import Espacio
from schemas import EspacioCrear, EspacioModificar

async def crear(db: AsyncSession, datos: EspacioCrear):
    espacio = Espacio(calle_id=datos.calle_id)
    db.add(espacio)
    await db.commit()
    await db.refresh(espacio)
    return espacio

async def obtener_por_id(db: AsyncSession, espacio_id: int):
    return await db.get(Espacio, espacio_id)

async def listar(db: AsyncSession, calle_id: Optional[int] = None):
    stmt = select(Espacio)
    if calle_id:
        stmt = stmt.where(Espacio.calle_id == calle_id)
    resultado = await db.execute(stmt)
    return resultado.scalars().all()

async def modificar(db: AsyncSession, espacio: Espacio, datos: EspacioModificar):
    if datos.calle_id is not None:
        espacio.calle_id = datos.calle_id
    if datos.ocupado is not None:
        espacio.ocupado = datos.ocupado
    await db.commit()
    await db.refresh(espacio)
    return espacio

async def cambiar_estado(db: AsyncSession, espacio: Espacio, ocupado: bool):
    espacio.ocupado = ocupado
    await db.commit()
    await db.refresh(espacio)
    return espacio