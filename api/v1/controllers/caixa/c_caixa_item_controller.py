from typing import Optional, List
from fastapi import HTTPException, status # Importe HTTPException e status

# Schemas usados para entrada e saída de dados dos items
from api.v1.schemas.caixa.c_caixa_item_schema import (
    CCaixaItemSchemaBase,
    CCaixaItemSchemaList,
    CCaixaItemPaginationSchema
)

# Model responsável pelo acesso ao banco de dados Firebird
from api.v1.models.caixa.c_caixa_item_model import CCaixaItemModel

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from core.validation import InputSanitizer

# Retorna a lista de todos os itens cadastrados
def get_all_caixa_itens(skip: int = 0, limit: int = 10) -> CCaixaItemPaginationSchema:
    try:
        itens = CCaixaItemModel.get_all_caixa_itens(skip=skip, limit=limit)
        total = CCaixaItemModel.count_items()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [CCaixaItemSchemaList(**u) for u in itens]            
        }
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao listar os itens: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao listar os itens: {e}"
        )
    
# Retorna a quantidade de registros no banco de dados
def count_items() -> int:
    try:
        return CCaixaItemModel.count_items()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao contar items: {e}"
        )

# Retorna um item específico pelo ID
def get_item_by_id(caixa_item_id: int) -> CCaixaItemSchemaBase: # Retorno alterado para UserSchemaBase
    try:
        item = CCaixaItemModel.get_by_id(caixa_item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item com ID {caixa_item_id} não encontrado."
            )
        return CCaixaItemSchemaBase(**item)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao buscar item por ID: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao buscar item por ID: {e}"
        )    