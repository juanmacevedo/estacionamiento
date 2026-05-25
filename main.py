from fastapi import FastAPI
from routers import calles, espacios, vehiculos, ocupaciones
from routers import admin

app = FastAPI()

app.include_router(admin.router)
app.include_router(calles.router)
app.include_router(espacios.router)
app.include_router(vehiculos.router)
app.include_router(ocupaciones.router)