from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List

from core.deps import get_session, get_current_user
from models.cachorro_model import CachorroModel
from models.usuario_model import UsuarioModel
from schemas.cachorro_schema import CachorroSchema, CachorroUpSchema

router = APIRouter()

@router.post("/", response_model=CachorroSchema, status_code=status.HTTP_201_CREATED)
async def post_cachorro(cachorro: CachorroSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    novo_cachorro: CachorroModel = CachorroModel(nome=cachorro.nome, raca=cachorro.raca, idade=cachorro.idade, dono=cachorro.id, usuario=usuario_logado.id)

    async with db as session:
        session.add(novo_cachorro)
        await session.commit()

        return novo_cachorro

@router.get("/", response_model=List[CachorroSchema], status_code=status.HTTP_200_OK)
async def get_cachorros(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CachorroModel)
        result = await session.execute(query)
        cachorros: List[CachorroSchema] = result.scalars().unique().all()

        return cachorros

@router.get("/{cachorro_id}", response_model=CachorroSchema, status_code=status.HTTP_200_OK)
async def get_cachorro(cachorro_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CachorroModel).filter(CachorroModel.id == cachorro_id)
        result = await session.execute(query)
        cachorro: CachorroSchema = result.scalars().unique().one_or_none()

        if cachorro:
            return cachorro
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cachorro não encontrado.")

@router.put("/{cachorro_id}", response_model=CachorroSchema, status_code=status.HTTP_200_OK)
async def put_cachorro(cachorro_id: int, cachorro: CachorroUpSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CachorroModel).filter(CachorroModel.id == cachorro_id)
        result = await session.execute(query)
        cachorro_up: CachorroSchema = result.scalars().unique().one_or_none()

        if cachorro_up:
            if cachorro.nome:
                cachorro_up.nome = cachorro.nome
            if cachorro.raca:
                cachorro_up.raca = cachorro.raca
            if cachorro.idade:
                cachorro_up.idade = cachorro.idade
            if cachorro.usuario_id != usuario_logado.id:
                cachorro_up.usuario_id = usuario_logado.id

            await session.commit()
            return cachorro_up
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cachorro não encontrado.")


@router.delete("/{cachorro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cachorro(cachorro_id: int, db: AsyncSession = Depends(get_session),
                       usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CachorroModel).filter(CachorroModel.id == cachorro_id)
        result = await session.execute(query)
        cachorro_del: CachorroSchema = result.scalars().unique().one_or_none()

        if cachorro_del:
            await session.delete(cachorro_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cachorro não encontrado.")
