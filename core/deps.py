# core/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.configs import settings
from api.v1.models.g_usuario_model import UserModel # <--- Importe o UserModel

# Define o esquema de segurança OAuth2 (token tipo Bearer)
oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

# Função que retorna o usuário autenticado com base no token JWT
def get_current_user(token: str = Depends(oauth2_schema)) -> dict:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    # --- NOVO: Buscar os dados completos do usuário do banco de dados ---
    # Convert user_id para int, se ele for um string no JWT e int no banco
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format in token."
        )

    # Use o UserModel para buscar os dados completos
    # Adicione um try-except para a chamada ao modelo para capturar erros de DB
    try:
        user = UserModel.get_by_id(user_id_int)
    except Exception as e: # Captura qualquer erro ao buscar no DB
        print(f"Error fetching user in get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user data. {str(e)}"
        )

    if not user:
        # Se o usuário não for encontrado no DB (mas o token era válido para um ID),
        # pode indicar um usuário deletado ou um ID inválido no token.
        raise credential_exception # Ou HTTPException(404, "User associated with token not found")

    return user # Retorna o dicionário completo do usuário