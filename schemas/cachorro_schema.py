from pydantic import BaseModel, ConfigDict

from typing import Optional, List

class CachorroSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    nome: str
    raca: str
    idade: int