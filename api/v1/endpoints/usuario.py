from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session, get_current_user
from core.security import gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchema, UsuarioCreateSchema, UsuarioUpSchema

router = APIRouter()

@router.get("/logado", response_model=UsuarioSchema)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado

@router.post("/signup", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioCreateSchema, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome,sobrenome=usuario.sobrenome,email=usuario.email,senha=gerar_hash_senha(usuario.senha), eh_admin=usuario.eh_admin)

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuário já cadastrado.")

@router.get("/", response_model=List[UsuarioSchema], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchema] = result.scalars().unique().all()

        return usuarios

@router.get("/{usuario_id}", response_model=UsuarioSchema, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")


@router.put("/{usuario_id}", response_model=UsuarioSchema, status_code=status.HTTP_200_OK)
async def put_usuario(usuario_id: int, usuario: UsuarioUpSchema, db: AsyncSession = Depends(get_session),
                      usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioUpSchema = result.scalars().unique().one_or_none()

        if usuario_up:
            if usuario.nome:
                usuario_up.nome = usuario.nome
            if usuario.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario.email:
                usuario_up.email = usuario.email
            if usuario.senha:
                usuario_up.senha = gerar_hash_senha(usuario.senha)
            if usuario.eh_admin:
                usuario_up.eh_admin = usuario.eh_admin

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session),
                      usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.usuario_id == usuario_id).filter(UsuarioModel.usuario_id != usuario_logado.id)
        result = await session.execute(query)
        usuario_del: UsuarioSchema = result.scalars().unique().one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password,db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de acesso incorretos.")

    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)