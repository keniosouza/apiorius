# schemas/g_usuario_schema.py

from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema base usado para representar um usuário retornado pela API
class UserSchemaBase(BaseModel):
    user_id: Optional[int] = None       # ID do usuário (opcional)
    nome_completo: Optional[str] = None     # Nome completo do usuário
    email: Optional[EmailStr] = None    # E-mail validado do usuário

    class Config:
        from_attributes = True  # Permite construir a partir de dicts ou ORMs (mesmo sem ORM aqui)


# Schema usado para criação de um novo usuário
class UserSchemaCreate(BaseModel):
    nome_completo: str                    # Nome completo obrigatório
    email: EmailStr                   # E-mail obrigatório e validado
    senha_api: str                     # Senha enviada pelo cliente (será criptografada no backend)


# Schema usado para atualização de dados do usuário
# Todos os campos são opcionais para permitir atualizações parciais
class UserSchemaUpdate(BaseModel):
    nome_completo: Optional[str] = None   # Atualização do nome, se fornecido
    email: Optional[EmailStr] = None  # Atualização do e-mail, se fornecido
    senha_api: Optional[str] = None    # Atualização da senha, se fornecida

    class Config:
        from_attributes = True


# Schema para listagem de registros com paginação
class UserSchemaList(BaseModel):
    usuario_id: float  # USUARIO_ID NUMERIC(10,2)
    trocarsenha: Optional[str]
    login: Optional[str]
    situacao: Optional[str]
    nome_completo: Optional[str]
    funcao: Optional[str]
    assina: Optional[str]
    sigla: Optional[str]
    usuario_tab: Optional[float]  # NUMERIC(10,2)
    ultimo_login: Optional[datetime]
    ultimo_login_regs: Optional[datetime]
    data_expiracao: Optional[datetime]
    andamento_padrao: Optional[float]  # NUMERIC(10,2)
    lembrete_pergunta: Optional[str]
    lembrete_resposta: Optional[str]
    andamento_padrao2: Optional[float]  # NUMERIC(10,2)
    receber_mensagem_arrolamento: Optional[str]
    email: Optional[EmailStr]  # ou Optional[str] se preferir mais flexível
    assina_certidao: Optional[str]
    receber_email_penhora: Optional[str]
    foto: Optional[bytes]  # BLOB SUB_TYPE BINARY
    nao_receber_chat_todos: Optional[str]
    pode_alterar_caixa: Optional[str]
    receber_chat_certidao_online: Optional[str]
    receber_chat_cancelamento: Optional[str]
    cpf: Optional[str]
    somente_leitura: Optional[str]
    receber_chat_envio_onr: Optional[str]
    tipo_usuario: Optional[str]
    data_cadastro: Optional[datetime]


class UserPaginationSchema(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[UserSchemaList]
