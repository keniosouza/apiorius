# main.py

# Ajuste para garantir que o diretório base do projeto seja incluído no PYTHONPATH
import sys
import os

# Adiciona o diretório atual (onde está o main.py) ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa a classe principal do FastAPI
from fastapi import FastAPI

# Importa as configurações globais da aplicação
from core.configs import settings

# Importa o roteador principal da API versão 1
from api.v1.api import api_router

# Instancia o app FastAPI com um título personalizado
app = FastAPI(title='Orius Cartórios')

# Inclui as rotas da versão 1 da API com prefixo definido em settings (ex: /api/v1)
app.include_router(api_router, prefix=settings.API_V1_STR)

# Executa o servidor com Uvicorn se este arquivo for executado diretamente
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",           # Caminho do app para execução
        host="0.0.0.0",       # Disponibiliza a aplicação externamente
        port=8000,            # Porta padrão
        log_level='info',     # Define o nível de log para desenvolvimento
        reload=True           # Ativa auto-reload durante desenvolvimento
    )
