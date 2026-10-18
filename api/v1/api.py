from fastapi import APIRouter

from api.v1.endpoints import dono
from api.v1.endpoints import cachorro
from api.v1.endpoints import usuario

api_router = APIRouter()

api_router.include_router(dono.router, prefix="/donos", tags=["donos"])
api_router.include_router(cachorro.router, prefix="/cachorros", tags=["cachorros"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["usuarios"])