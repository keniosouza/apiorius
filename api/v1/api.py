from fastapi import APIRouter  # Importa o gerenciador de rotas do FastAPI

# Importa os módulos de rotas específicos
from api.v1.endpoints import g_usuario_endpoint
from api.v1.endpoints import c_caixa_item_endpoint

# Cria uma instância do APIRouter que vai agregar todas as rotas da API
api_router = APIRouter()

# Inclui as rotas de "g_usuario" no roteador principal, com prefixo /usuarios e tag 'Usuarios'
api_router.include_router(
    g_usuario_endpoint.router, prefix='/usuarios', tags=['Usuários']
)

# Inclui as rotas de "c_caixa_item no roteador principal, com prefixo /c_caixa_items e tag 'Caixa Itens'
api_router.include_router(
    c_caixa_item_endpoint.router, prefix='/caixa_itens', tags=['Caixa Itens']
)