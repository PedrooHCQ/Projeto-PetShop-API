from pydantic import BaseModel, ConfigDict

from typing import Optional, List

class UsuarioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: str
    eh_admin: Optional[bool]

class UsuarioCreateSchema(UsuarioSchema):
    senha: str

class UsuarioUpSchema(UsuarioSchema):
    id: Optional[int]
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[str]
    senha: Optional[str]
    eh_admin: Optional[bool]
