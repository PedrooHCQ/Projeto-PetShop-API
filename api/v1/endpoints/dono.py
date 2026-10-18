from fastapi import APIRouter, Depends, HTTPException, status, Response

from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.deps import get_session, get_current_user
from models.dono_model import DonoModel
from models.usuario_model import UsuarioModel
from schemas.dono_schema import DonoSchema, DonoCachorrosSchema, DonoUpSchema

router = APIRouter()

@router.post("/", response_model=DonoSchema, status_code=status.HTTP_201_CREATED)
async def post_donos(dono: DonoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    novo_dono: UsuarioModel = UsuarioModel(cpf=dono.cpf, nome=dono.nome, sobrenome=dono.sobrenome, telefone=dono.telefone, endereco=dono.endereco)

    async with db as session:
        try:
            session.add(novo_dono)
            await session.commit()

            return novo_dono
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Usuário já existe no sistema")

@router.get("/", response_model=List[DonoSchema], status_code=status.HTTP_200_OK)
async def get_donos(db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel)
        results = await session.execute(query)
        donos: List[DonoSchema] = results.scalars().unique().all()

        return donos

@router.get("/{cpf_dono}", status_code=status.HTTP_200_OK, response_model=DonoCachorrosSchema)
async def get_dono(cpf_dono: str, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.cpf == cpf_dono)
        result = await session.execute(query)
        dono: DonoSchema = result.scalars().unique().one_or_none()

        if dono:
            return dono
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")

@router.put("/{cpf_dono}", status_code=status.HTTP_202_ACCEPTED, response_model=DonoSchema)
async def put_dono(cpf_dono: str, dono: DonoUpSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.cpf == cpf_dono)
        result = await session.execute(query)
        dono_up: DonoSchema = result.scalars().unique().one_or_none()

        if dono_up:
            if dono.cpf:
                dono_up.cpf = dono.cpf
            if dono.nome:
                dono_up.nome = dono.nome
            if dono.sobrenome:
                dono_up.sobrenome = dono.sobrenome
            if dono.telefone:
                dono_up.telefone = dono.telefone
            if dono.endereco:
                dono_up.endereco = dono.endereco

            await session.commit()

            return dono
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")


@router.delete("/{cpf_dono}", status_code=status.HTTP_204_NO_CONTENT)
async def get_dono(cpf_dono: str, db: AsyncSession = Depends(get_session),
                   usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.cpf == cpf_dono)
        result = await session.execute(query)
        dono_del: DonoSchema = result.scalars().unique().one_or_none()

        if dono_del:
            await session.delete(dono_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")

@router.get("/{dono_id}", status_code=status.HTTP_200_OK, response_model=DonoCachorrosSchema)
async def get_dono(dono_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.id == dono_id)
        result = await session.execute(query)
        dono: DonoSchema = result.scalars().unique().one_or_none()

        if dono:
            return dono
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")

@router.put("/{dono_id}", status_code=status.HTTP_202_ACCEPTED, response_model=DonoSchema)
async def put_dono(dono_id: int, dono: DonoUpSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.id == dono_id)
        result = await session.execute(query)
        dono_up: DonoSchema = result.scalars().unique().one_or_none()

        if dono_up:
            if dono.cpf:
                dono_up.cpf = dono.cpf
            if dono.nome:
                dono_up.nome = dono.nome
            if dono.sobrenome:
                dono_up.sobrenome = dono.sobrenome
            if dono.telefone:
                dono_up.telefone = dono.telefone
            if dono.endereco:
                dono_up.endereco = dono.endereco

            await session.commit()

            return dono
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")

@router.delete("/{dono_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_dono(dono_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(DonoModel).filter(DonoModel.id == dono_id)
        result = await session.execute(query)
        dono_del: DonoSchema = result.scalars().unique().one_or_none()

        if dono_del:
            await session.delete(dono_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dono não encontrado.")