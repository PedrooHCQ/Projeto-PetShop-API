from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import DBBaseModel

class UsuarioModel(DBBaseModel):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    sobrenome = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, index=True, unique=True)
    senha = Column(String(256), nullable=False)
    eh_admin = Column(Boolean, nullable=False, default=False)

    cachorros = relationship('CachorroModel',
                             cascade='all, delete-orphan',
                             back_populates='criador',
                             uselist=False,
                             lazy="joined")