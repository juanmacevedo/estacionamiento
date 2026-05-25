from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Optional, Union, Any
from models import Ocupacion
from schemas import OcupacionCrear
from repository import ocupaciones as ocupaciones_repo
from services import espacios as espacios_service
from services import vehiculos as vehiculos_service
from config import UNIDAD_TIEMPO

async def listar_ocupaciones(db: AsyncSession, vehiculo_id: Optional[int] = None, espacio_id: Optional[int] = None, finalizadas: Optional[bool] = None):
    return await ocupaciones_repo.listar(db, vehiculo_id, espacio_id, finalizadas)

async def obtener_ocupacion(db: AsyncSession, ocupacion_id: int):
    ocupacion = await ocupaciones_repo.obtener_por_id(db, ocupacion_id)
    if not ocupacion:
        raise HTTPException(status_code=404, detail="Ocupacion no encontrada")
    return ocupacion

async def consultar_disponibilidad(db: AsyncSession, fecha_inicio: datetime, fecha_fin: datetime, calle_id: Optional[int] = None, espacio_id: Optional[int] = None):
    espacios = await espacios_service.listar_espacios(db, calle_id)

    if espacio_id is not None:
        espacios = [e for e in espacios if e.id == espacio_id]

    if not espacios:
        raise HTTPException(status_code=404, detail="No se encontraron espacios")

    espacio_ids = [e.id for e in espacios]
    ocupados = await ocupaciones_repo.obtener_espacios_ocupados_en_rango(db, fecha_inicio, fecha_fin, espacio_ids)
    disponibles = [e for e in espacios if e.id not in ocupados]
    return {"disponibles": [e.id for e in disponibles]}

async def _tiene_conflicto_vehiculo(db: AsyncSession, vehiculo_id: int, fecha_inicio: datetime, fecha_fin: datetime):
    ahora = datetime.now()
    ocupaciones = await ocupaciones_repo.listar(db, vehiculo_id=vehiculo_id)
    for o in ocupaciones:
        o_fin = o.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:o.duracion_horas})
        if o.fecha_fin is not None:
            continue
        if o_fin <= ahora:
            continue
        if o.fecha_inicio < fecha_fin and o_fin > fecha_inicio:
            return True
    return False

async def _validar_enfriamiento(db: AsyncSession, vehiculo_id: int, calle_id: int, fecha_inicio: datetime, duracion_horas: int):
    fecha_fin_nueva = fecha_inicio + timedelta(**{UNIDAD_TIEMPO:duracion_horas})
    inicio_protegido = fecha_inicio - timedelta(**{UNIDAD_TIEMPO:1})
    fin_protegido = fecha_fin_nueva + timedelta(**{UNIDAD_TIEMPO:1})

    ocupaciones = await ocupaciones_repo.listar(db, vehiculo_id=vehiculo_id)

    for o in ocupaciones:
        espacio = await espacios_service.obtener_espacio(db, o.espacio_id)
        if espacio.calle_id != calle_id:
            continue
        o_fin = o.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:o.duracion_horas})
        if o.fecha_inicio < fin_protegido and o_fin > inicio_protegido:
            raise HTTPException(status_code=400, detail="Debe respetar 1 hora de enfriamiento en esta calle")

async def registrar_ocupacion(db: AsyncSession, datos: OcupacionCrear):
    ahora = datetime.now()
    fecha_fin_nueva = datos.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:datos.duracion_horas})

    # 1. vehiculo existe
    await vehiculos_service.obtener_vehiculo(db, datos.vehiculo_id)

    # 2. espacio existe
    espacio = await espacios_service.obtener_espacio(db, datos.espacio_id)

    # 3. espacio disponible
    if espacio.ocupado:
        raise HTTPException(status_code=400, detail="Espacio ocupado")

    # 4. fecha_inicio no en el pasado con 30 segundos de tolerancia
    if datos.fecha_inicio < ahora - timedelta(seconds=30):
        raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser en el pasado")

    # 5. maximo 48hs de anticipacion
    if datos.fecha_inicio > ahora + timedelta(**{UNIDAD_TIEMPO:48}):
        raise HTTPException(status_code=400, detail="No se puede reservar con mas de 48hs de anticipacion")

    # 6. duracion entre 1 y 4hs
    if datos.duracion_horas > 4 or datos.duracion_horas < 1:
        raise HTTPException(status_code=400, detail="La duracion debe ser entre 1 y 4 horas")

    # 7. espacio sin conflicto de rango
    disponible = await ocupaciones_repo.obtener_espacios_ocupados_en_rango(db, datos.fecha_inicio, fecha_fin_nueva, [datos.espacio_id])
    if datos.espacio_id in disponible:
        raise HTTPException(status_code=400, detail="El espacio no esta disponible en ese horario")

    # 8. vehiculo sin conflicto de rango
    if await _tiene_conflicto_vehiculo(db, datos.vehiculo_id, datos.fecha_inicio, fecha_fin_nueva):
        raise HTTPException(status_code=400, detail="El vehiculo ya tiene una ocupacion en ese horario")

    # 9. maximo 1 reserva futura activa
    ocupaciones_vehiculo = await ocupaciones_repo.listar(db, vehiculo_id=datos.vehiculo_id)
    reservas_futuras = [
        o for o in ocupaciones_vehiculo
        if o.fecha_inicio > ahora and o.fecha_fin is None
    ]
    if len(reservas_futuras) >= 1:
        raise HTTPException(status_code=400, detail="Ya tiene una reserva futura activa")

    # 10 y 11. enfriamiento en misma calle
    await _validar_enfriamiento(db, datos.vehiculo_id, espacio.calle_id, datos.fecha_inicio, datos.duracion_horas)

    return await ocupaciones_repo.crear(db, datos.vehiculo_id, datos.espacio_id, datos.fecha_inicio, datos.duracion_horas)

async def iniciar_ocupacion(db: AsyncSession, ocupacion_id: int) -> Union[Ocupacion, dict[str, Any]]:
    ahora = datetime.now()
    ocupacion = await obtener_ocupacion(db, ocupacion_id)

    if ocupacion.fecha_fin is not None:
        raise HTTPException(status_code=400, detail="La ocupacion ya fue finalizada")

    if ocupacion.fecha_inicio > ahora:
        raise HTTPException(status_code=400, detail="La ocupacion aun no inicio")

    fecha_fin_prevista = ocupacion.fecha_inicio + timedelta(**{UNIDAD_TIEMPO:ocupacion.duracion_horas})
    if ahora > fecha_fin_prevista:
        raise HTTPException(status_code=400, detail="La ocupacion ya expiro")

    espacio = await espacios_service.obtener_espacio(db, ocupacion.espacio_id)

    if espacio.ocupado:
        await ocupaciones_repo.eliminar(db, ocupacion)
        return {"mensaje": "Espacio ocupado por razon externa, se emite reembolso"}

    await espacios_service.cambiar_estado(db, ocupacion.espacio_id, True)
    return ocupacion

async def finalizar_ocupacion(db: AsyncSession, ocupacion_id: int) -> Union[Ocupacion, dict[str, Any]]:
    ahora = datetime.now().replace(microsecond=0)
    ocupacion = await obtener_ocupacion(db, ocupacion_id)

    if ocupacion.fecha_fin is not None:
        raise HTTPException(status_code=400, detail="La ocupacion ya fue finalizada")

    if ocupacion.fecha_inicio > ahora:
        await ocupaciones_repo.eliminar(db, ocupacion)
        return {"mensaje": "Reserva cancelada"}

    resultado = await ocupaciones_repo.finalizar(db, ocupacion, ahora)
    await espacios_service.cambiar_estado(db, ocupacion.espacio_id, False)
    return resultado
