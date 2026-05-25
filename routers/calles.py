from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import calles as calles_service

router = APIRouter(prefix="/calles", tags=["calles"])

@router.post("/")
async def crear_calle(db: Annotated[AsyncSession, Depends(get_db)]):
    return await calles_service.crear_calle(db)