from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CalleRespuesta(BaseModel):
    id: int

class EspacioCrear(BaseModel):
    calle_id: int

class EspacioRespuesta(BaseModel):
    id: int
    ocupado: bool
    calle_id: int

class EspacioModificar(BaseModel):
    calle_id: Optional[int] = None
    ocupado: Optional[bool] = None

class VehiculoRespuesta(BaseModel):
    id: int

class OcupacionCrear(BaseModel):
    vehiculo_id: int
    espacio_id: int
    fecha_inicio: datetime
    duracion_horas: int

class OcupacionRespuesta(BaseModel):
    id: int
    vehiculo_id: int
    espacio_id: int
    fecha_inicio: datetime
    duracion_horas: int
    fecha_fin: Optional[datetime] = None