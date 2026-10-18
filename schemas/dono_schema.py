from pydantic import BaseModel, ConfigDict

from typing import Optional, List

from schemas.cachorro_schema import CachorroSchema

class DonoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    cpf: str
    nome: str
    sobrenome: str
    telefone: str
    endereco: str

class DonoCachorrosSchema(DonoSchema):
    cachorros: Optional[List[CachorroSchema]]

class DonoUpSchema(DonoSchema):
    id: Optional[int] = None
    cpf: Optional[str] = None
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None