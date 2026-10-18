from idlelib import query

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.configs import settings
from core.security import verificar_senha

from models.usuario_model import UsuarioModel

from pydantic import EmailStr

from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")

async def autenticar(email: EmailStr,senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None

        return usuario