from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import vehiculos as vehiculos_repo

async def registrar_vehiculo(db: AsyncSession):
    return await vehiculos_repo.crear(db)

async def obtener_vehiculo(db: AsyncSession, vehiculo_id: int):
    vehiculo = await vehiculos_repo.obtener_por_id(db, vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")
    return vehiculo