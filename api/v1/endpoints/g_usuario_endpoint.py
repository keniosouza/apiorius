# endpoints/g_usuario_endpoint.py

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# Schemas para entrada e saída de dados (nomes padronizados em inglês)
from api.v1.schemas.g_usuario_schema import (
    UserSchemaBase,
    UserSchemaCreate,
    UserSchemaUpdate,
    UserPaginationSchema
)

# Controller responsável pelas regras de negócio e sanitização
from api.v1.controllers.g_usuario_controller import (
    authenticate_user,
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    count_users
)

# Dependência para obter o usuário autenticado a partir do token JWT      
from core.deps import get_current_user

# Função para gerar JWT
from core.auth import create_access_token

# Inicializa o roteador responsável pelas rotas de usuários
router = APIRouter()


# ---------------------- ROTAS FIXAS ----------------------

@router.get('/logado', response_model=UserSchemaBase)
def get_logged_user(current_user: dict = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado com o token atual.
    """
    return current_user


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
def post_user(user: UserSchemaCreate):
    """
    Cria um novo usuário após validações e sanitizações.
    """
    new_user = create_user(user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='E-mail is already registered.'
        )
    return new_user


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Realiza login com e-mail e senha, retornando um token JWT válido.
    """
    user = authenticate_user(
        email=form_data.username,
        senha_api=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid login credentials.'
        )

    return JSONResponse(content={
        "access_token": create_access_token(sub=user["user_id"]),
        "token_type": "bearer",
    })


# ---------------------- ROTAS DINÂMICAS ----------------------

@router.get('/', response_model=UserPaginationSchema)
def get_users(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os usuários cadastrados no sistema.
    """
    usuarios = get_all_users(skip=skip, limit=limit)
    total = count_users()

    return get_all_users(skip=skip, limit=limit)


@router.get('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    """
    Retorna os dados de um usuário específico pelo ID.
    """
    user = get_user_by_id(user_id)
    if user:
        return user

    raise HTTPException(
        detail='User not found.',
        status_code=status.HTTP_404_NOT_FOUND
    )


@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
def put_user(user_id: int, user: UserSchemaUpdate, current_user: dict = Depends(get_current_user)):
    """
    Atualiza os dados de um usuário específico com os campos fornecidos.
    """
    updated_user = update_user(user_id, user)
    if updated_user:
        return updated_user

    raise HTTPException(
        detail='User not found.',
        status_code=status.HTTP_404_NOT_FOUND
    )


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(user_id: int):
    """
    Exclui um usuário com base no ID fornecido.
    """
    success = delete_user(user_id)
    if success:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        detail='User not found.',
        status_code=status.HTTP_404_NOT_FOUND
    )
