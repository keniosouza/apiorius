# endpoints/c_caixa_item_endpoint.py

from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# Schemas para entrada e saída de dados (nomes padronizados em inglês)
from api.v1.schemas.caixa.c_caixa_item_schema import (
    CCaixaItemSchemaBase,
    CCaixaItemSchemaList,
    CCaixaItemPaginationSchema
)

# Controller responsável pelas regras de negócio e sanitização
from api.v1.controllers.caixa.c_caixa_item_controller import (
    get_all_caixa_itens,
    get_item_by_id,
    count_items
)

# Dependência para obter o usuário autenticado a partir do token JWT      
from core.deps import get_current_user

# Inicializa o roteador responsável pelas rotas de usuários
router = APIRouter()



# ---------------------- ROTAS DINÂMICAS ----------------------

@router.get('/', response_model=CCaixaItemPaginationSchema)
def get_items(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1), current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os usuários cadastrados no sistema.
    """
    items = get_all_caixa_itens(skip=skip, limit=limit)
    total = count_items()

    return get_all_caixa_itens(skip=skip, limit=limit)


@router.get('/{caixa_item_id}', response_model=CCaixaItemSchemaBase, status_code=status.HTTP_200_OK)
def get_user(caixa_item_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna os dados de um caixa item específico pelo ID.
    """
    item = get_item_by_id(caixa_item_id)
    if item:
        return item

    raise HTTPException(
        detail='User not found.',
        status_code=status.HTTP_404_NOT_FOUND
    )
