from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from database import get_db
from schemas import OcupacionCrear
from services import ocupaciones as ocupaciones_service

router = APIRouter(prefix="/ocupaciones", tags=["ocupaciones"])

@router.post("/")
async def registrar_ocupacion(datos: OcupacionCrear, db: Annotated[AsyncSession, Depends(get_db)]):
    datos.fecha_inicio = datos.fecha_inicio.replace(tzinfo=None)
    return await ocupaciones_service.registrar_ocupacion(db, datos)

@router.get("/")
async def listar_ocupaciones(
    db: Annotated[AsyncSession, Depends(get_db)],
    vehiculo_id: Optional[int] = None,
    espacio_id: Optional[int] = None,
    finalizadas: Optional[bool] = None
):
    return await ocupaciones_service.listar_ocupaciones(db, vehiculo_id, espacio_id, finalizadas)
    return await ocupaciones_service.listar_ocupaciones(db, vehiculo_id, espacio_id)

@router.post("/{ocupacion_id}/iniciar")
async def iniciar_ocupacion(ocupacion_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await ocupaciones_service.iniciar_ocupacion(db, ocupacion_id)

@router.post("/{ocupacion_id}/finalizar")
async def finalizar_ocupacion(ocupacion_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await ocupaciones_service.finalizar_ocupacion(db, ocupacion_id)

@router.get("/disponibilidad")
async def consultar_disponibilidad(
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Annotated[AsyncSession, Depends(get_db)],
    calle_id: Optional[int] = None,
    espacio_id: Optional[int] = None
):
    fecha_inicio = fecha_inicio.replace(tzinfo=None)
    fecha_fin = fecha_fin.replace(tzinfo=None)
    return await ocupaciones_service.consultar_disponibilidad(db, fecha_inicio, fecha_fin, calle_id, espacio_id)