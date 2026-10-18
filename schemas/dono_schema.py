from pydantic import BaseModel, ConfigDict

from typing import Optional

class DonoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    nome: str
    sobrenome: str
    telefone: str
    endereco: str