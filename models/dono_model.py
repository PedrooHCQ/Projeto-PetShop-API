from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.configs import DBBaseModel

class DonoModel(DBBaseModel):
    __tablename__ = 'donos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(11), nullable=False, unique=True)
    nome = Column(String(256), nullable=False)
    sobrenome = Column(String(256), nullable=False)
    telefone = Column(String(256), nullable=False)
    endereco = Column(String(256), nullable=False)
    cachorros = relationship("CachorrosModel",
                           cascade="all, delete-orphan",
                           back_populates="dono",
                           uselist=True,
                           lazy="joined")