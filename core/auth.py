from pytz import timezone
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from core.configs import settings
from api.v1.controllers.g_usuario_controller import authenticate_user

# Define o esquema OAuth2 para login
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

# Função para criar um token JWT
def create_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


# Criação do token de acesso (access_token)
def create_access_token(sub: str) -> str:
    return create_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
