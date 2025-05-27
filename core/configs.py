from pydantic_settings import BaseSettings

# Classe de configurações gerais da aplicação
class Settings(BaseSettings):
    # Prefixo padrão para as rotas da API
    API_V1_STR: str = '/api/v1'

    # URL de conexão com o banco de dados Firebird 4 (driver oficial)
    # Obs: encode a senha corretamente se houver caracteres especiais
    # DB_URL: str = 'firebird://SYSDBA:SW0WJclCDVMhlMviu%2BRI@api_firebird:3050/CARTORIO'
    DB_URL: str = "firebird://SYSDBA:Sun147oi.@api_firebird/3050:/var/lib/firebird/data/CARTORIO.FDB"


    # Chave secreta usada para geração de tokens JWT
    JWT_SECRET: str = 'WYe1zwtlDkh39_X3X3qTSICFDxts4VQrMyGLxnEpGUg'

    """
    Para gerar uma nova chave JWT segura, use:
    import secrets
    secrets.token_urlsafe(32)
    """

    # Algoritmo usado para assinar os tokens JWT
    ALGORITHM: str = 'HS256'

    # Tempo de expiração do token JWT (em minutos): 1 semana 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # Configuração do Pydantic
    class Config:
        case_sensitive = True  # Variáveis de ambiente sensíveis a maiúsculas/minúsculas

# Instância global das configurações
settings: Settings = Settings()