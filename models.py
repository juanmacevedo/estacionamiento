from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Boolean
from datetime import datetime
from typing import Optional
from database import Base

class Calle(Base):
    __tablename__ = "calles"

    id: Mapped[int] = mapped_column(primary_key=True)
    espacios: Mapped[list["Espacio"]] = relationship(back_populates="calle")

class Espacio(Base):
    __tablename__ = "espacios"

    id: Mapped[int] = mapped_column(primary_key=True)
    ocupado: Mapped[bool] = mapped_column(Boolean, default=False)
    calle_id: Mapped[int] = mapped_column(ForeignKey("calles.id"))
    calle: Mapped["Calle"] = relationship(back_populates="espacios")
    ocupaciones: Mapped[list["Ocupacion"]] = relationship(back_populates="espacio")

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(primary_key=True)
    ocupaciones: Mapped[list["Ocupacion"]] = relationship(back_populates="vehiculo")

class Ocupacion(Base):
    __tablename__ = "ocupaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"))
    espacio_id: Mapped[int] = mapped_column(ForeignKey("espacios.id"))
    fecha_inicio: Mapped[datetime]
    duracion_horas: Mapped[int]
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    vehiculo: Mapped["Vehiculo"] = relationship(back_populates="ocupaciones")
    espacio: Mapped["Espacio"] = relationship(back_populates="ocupaciones")