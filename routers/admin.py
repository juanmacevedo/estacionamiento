from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/reset")
async def reset_db(db: Annotated[AsyncSession, Depends(get_db)]):
    await db.execute(text("TRUNCATE TABLE ocupaciones, espacios, vehiculos, calles RESTART IDENTITY CASCADE"))
    await db.commit()
    return {"mensaje": "Base de datos reseteada"}