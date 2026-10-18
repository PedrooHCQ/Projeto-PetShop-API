from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import DBBaseModel

class CachorroModel(DBBaseModel):
    __tablename__ = 'cachorros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=False)
    raca = Column(String(256), nullable=False)
    idade = Column(Integer, nullable=False)
    dono_id = Column(Integer, ForeignKey('donos.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    dono = relationship('DonoModel', back_populates='cachorros', lazy="joined")
    criador = relationship('UsuarioModel', back_populates='cachorros', uselist=False, lazy="joined")
