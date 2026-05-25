from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import EspacioCrear, EspacioModificar
from typing import Optional
from repository import espacios as espacios_repo
from services import calles as calles_service

async def crear_espacio(db: AsyncSession, datos: EspacioCrear):
    await calles_service.obtener_calle(db, datos.calle_id)
    return await espacios_repo.crear(db, datos)

async def obtener_espacio(db: AsyncSession, espacio_id: int):
    espacio = await espacios_repo.obtener_por_id(db, espacio_id)
    if not espacio:
        raise HTTPException(status_code=404, detail="Espacio no encontrado")
    return espacio

async def listar_espacios(db: AsyncSession, calle_id: Optional[int] = None):
    return await espacios_repo.listar(db, calle_id)

async def modificar_espacio(db: AsyncSession, espacio_id: int, datos: EspacioModificar):
    espacio = await obtener_espacio(db, espacio_id)
    if datos.calle_id is not None:
        await calles_service.obtener_calle(db, datos.calle_id)
    return await espacios_repo.modificar(db, espacio, datos)

async def cambiar_estado(db: AsyncSession, espacio_id: int, ocupado: bool):
    espacio = await obtener_espacio(db, espacio_id)
    return await espacios_repo.cambiar_estado(db, espacio, ocupado)