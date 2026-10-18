from pydantic import BaseModel, ConfigDict

from typing import Optional, List

class CachorroSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    nome: str
    raca: str
    idade: int
    dono_id: Optional[int] = None
    usuario_id: Optional[int] = None

class CachorroUpSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    nome: Optional[str] = None
    raca: Optional[str] = None
    idade: Optional[int] = None
    usuario_id: Optional[int] = None