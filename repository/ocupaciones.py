from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
from models import Ocupacion
from config import UNIDAD_TIEMPO

async def crear(db: AsyncSession, vehiculo_id: int, espacio_id: int, fecha_inicio: datetime, duracion_horas: int):
    ocupacion = Ocupacion(
        vehiculo_id=vehiculo_id,
        espacio_id=espacio_id,
        fecha_inicio=fecha_inicio,
        duracion_horas=duracion_horas
    )
    db.add(ocupacion)
    await db.commit()
    await db.refresh(ocupacion)
    return ocupacion

async def obtener_por_id(db: AsyncSession, ocupacion_id: int):
    return await db.get(Ocupacion, ocupacion_id)

async def listar(db: AsyncSession, vehiculo_id: Optional[int] = None, espacio_id: Optional[int] = None, finalizadas: Optional[bool] = None):
    stmt = select(Ocupacion)
    if vehiculo_id:
        stmt = stmt.where(Ocupacion.vehiculo_id == vehiculo_id)
    if espacio_id:
        stmt = stmt.where(Ocupacion.espacio_id == espacio_id)
    if finalizadas is True:
        stmt = stmt.where(Ocupacion.fecha_fin != None)  # type: ignore
    elif finalizadas is False:
        stmt = stmt.where(Ocupacion.fecha_fin == None)  # type: ignore
    resultado = await db.execute(stmt)
    return resultado.scalars().all()

async def obtener_espacios_ocupados_en_rango(db: AsyncSession, fecha_inicio: datetime, fecha_fin: datetime, espacio_ids: list[int]):
    ahora = datetime.now()
    stmt = select(Ocupacion.espacio_id).where(
        Ocupacion.espacio_id.in_(espacio_ids),
        Ocupacion.fecha_fin == None,  # type: ignore
        Ocupacion.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:1}) * Ocupacion.duracion_horas > ahora,
        Ocupacion.fecha_inicio < fecha_fin,
        Ocupacion.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:1}) * Ocupacion.duracion_horas > fecha_inicio
    )
    resultado = await db.execute(stmt)
    return resultado.scalars().all()

async def finalizar(db: AsyncSession, ocupacion: Ocupacion, fecha_fin: datetime):
    ocupacion.fecha_fin = fecha_fin
    await db.commit()
    await db.refresh(ocupacion)
    return ocupacion

async def eliminar(db: AsyncSession, ocupacion: Ocupacion):
    await db.delete(ocupacion)
    await db.commit()

async def actualizar_espacio(db: AsyncSession, ocupacion: Ocupacion, espacio_id: int):
    ocupacion.espacio_id = espacio_id
    await db.commit()
    await db.refresh(ocupacion)
    return ocupacion