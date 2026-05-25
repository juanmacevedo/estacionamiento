from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import calles as calles_repo

async def crear_calle(db: AsyncSession):
    return await calles_repo.crear(db)

async def obtener_calle(db: AsyncSession, calle_id: int):
    calle = await calles_repo.obtener_por_id(db, calle_id)
    if not calle:
        raise HTTPException(status_code=404, detail="Calle no encontrada")
    return calle