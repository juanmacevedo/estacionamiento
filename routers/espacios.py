from fastapi import APIRouter, Depends
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import espacios as espacios_service
from schemas import EspacioCrear, EspacioModificar

router = APIRouter(prefix="/espacios", tags=["espacios"])

@router.post("/")
async def crear_espacio(datos: EspacioCrear, db: Annotated[AsyncSession, Depends(get_db)]):
    return await espacios_service.crear_espacio(db, datos)

@router.get("/")
async def listar_espacios(db: Annotated[AsyncSession, Depends(get_db)], calle_id: Optional[int] = None):
    return await espacios_service.listar_espacios(db, calle_id)

@router.patch("/{espacio_id}")
async def modificar_espacio(espacio_id: int, datos: EspacioModificar, db: Annotated[AsyncSession, Depends(get_db)]):
    return await espacios_service.modificar_espacio(db, espacio_id, datos)