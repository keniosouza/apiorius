# schemas/c_caixa_item_schema.py

from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal

# Schema base usado para representar um caixa_item retornado pela API
class CCaixaItemSchemaBase(BaseModel):
    caixa_item_id: Optional[int] = None
    descricao: Optional[str] = None
    data_pagamento: Optional[datetime] = None
    valor_servico: Optional[Decimal] = None
    valor_pago: Optional[Decimal] = None
    apresentante: Optional[str] = None

    class Config:
        from_attributes = True  # Permite construir a partir de dicts ou ORMs (mesmo sem ORM aqui)

# Schema para listagem de registros com paginação
class CCaixaItemSchemaList(BaseModel):
    caixa_item_id: Optional[int]
    descricao: Optional[str]
    data_pagamento: Optional[datetime]
    valor_servico: Optional[Decimal]
    valor_pago: Optional[Decimal]
    apresentante: Optional[str]


class CCaixaItemPaginationSchema(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[CCaixaItemSchemaList]        