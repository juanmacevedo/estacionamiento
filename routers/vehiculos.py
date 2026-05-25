from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import vehiculos as vehiculos_service

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])

@router.post("/")
async def registrar_vehiculo(db: Annotated[AsyncSession, Depends(get_db)]):
    return await vehiculos_service.registrar_vehiculo(db)