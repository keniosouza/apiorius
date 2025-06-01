# controllers/user_controller.py

from typing import Optional, List
from fastapi import HTTPException, status # Importe HTTPException e status

# Schemas usados para entrada e saída de dados dos usuários
from api.v1.schemas.g_usuario_schema import (
    UserSchemaBase,
    UserSchemaCreate,
    UserSchemaUpdate,
    UserSchemaList,
    UserPaginationSchema
)

# Model responsável pelo acesso ao banco de dados Firebird
from api.v1.models.g_usuario_model import UserModel

# Funções utilitárias para segurança (hash e verificação de senha)
from core.security import verify_senha_api, hash_senha_api

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from core.validation import InputSanitizer


# Autentica um usuário com base no e-mail e senha fornecidos
def authenticate_user(email: str, senha_api: str) -> Optional[dict]:
    # Nenhuma mudança significativa aqui, pois o retorno já é None ou dict
    email = InputSanitizer.clean_text(email)
    try:
        user = UserModel.get_by_email(email)
        if not user:
            return None # Não lança exceção para 'usuário não encontrado' em autenticação

        if not verify_senha_api(senha_api, user["senha_api"]):
            return None

        return user
    except RuntimeError as e:
        # Erros no banco de dados durante a busca, que podem ser tratados como 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao autenticar: {e}"
        )


# Cria um novo usuário após validação e sanitização dos campos
def create_user(user_data: UserSchemaCreate) -> UserSchemaBase: # Retorno alterado para UserSchemaBase, não Optional
    try:
        # Sanitiza os campos recebidos
        nome_completo = InputSanitizer.clean_text(user_data.nome_completo)
        email = InputSanitizer.clean_text(user_data.email)
        senha_api = InputSanitizer.clean_text(user_data.senha_api)

        # Validações iniciais (antes de ir para o banco)
        if not InputSanitizer.is_valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de e-mail inválido."
            )

        if not InputSanitizer.is_safe(nome_completo + email + senha_api):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conteúdo malicioso detectado nos dados do usuário."
            )

        hashed_senha_api = hash_senha_api(senha_api)

        # Chama o método do modelo, que agora pode levantar exceções
        result = UserModel.create(nome_completo, email, hashed_senha_api)

        # Se o modelo retornar um dicionário, converte para UserSchemaBase
        if result:
            return UserSchemaBase(**result)
        # Se o modelo retornasse None (o que não deve mais acontecer com as exceções),
        # poderia ser um erro interno ou algo que não previu.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Não foi possível criar o usuário por uma razão desconhecida."
        )

    except ValueError as e:
        # Captura erros de validação de dados do modelo (ex: e-mail duplicado, ou ID problemático)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflict para dados duplicados
            detail=str(e)
        )
    except RuntimeError as e:
        # Captura erros gerais de banco de dados ou problemas inesperados do modelo
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao criar usuário: {e}"
        )
    except Exception as e:
        # Captura qualquer outra exceção não tratada especificamente
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado: {e}"
        )


# Retorna a lista de todos os usuários cadastrados
def get_all_users(skip: int = 0, limit: int = 10) -> UserPaginationSchema:
    try:
        users = UserModel.get_all(skip=skip, limit=limit)
        total = UserModel.count_users()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": [UserSchemaList(**u) for u in users]            
        }
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao listar usuários: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao listar usuários: {e}"
        )

# Retorna a quantidade de registros no banco de dados
def count_users() -> int:
    try:
        return UserModel.count_users()
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao contar usuários: {e}"
        )

# Retorna um usuário específico pelo ID
def get_user_by_id(user_id: int) -> UserSchemaBase: # Retorno alterado para UserSchemaBase
    try:
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado."
            )
        return UserSchemaBase(**user)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao buscar usuário por ID: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao buscar usuário por ID: {e}"
        )


# Atualiza os dados de um usuário existente
def update_user(user_id: int, user_data: UserSchemaUpdate) -> UserSchemaBase: # Retorno alterado
    try:
        nome_completo = InputSanitizer.clean_text(user_data.nome_completo) if user_data.nome_completo else None
        email = InputSanitizer.clean_text(user_data.email) if user_data.email else None
        senha_api = InputSanitizer.clean_text(user_data.senha_api) if user_data.senha_api else None

        if email and not InputSanitizer.is_valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de e-mail inválido para atualização."
            )

        if any([nome_completo, email, senha_api]) and not InputSanitizer.is_safe(
            (nome_completo or '') + (email or '') + (senha_api or '')
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conteúdo malicioso detectado nos dados de atualização."
            )

        hashed_senha_api = hash_senha_api(senha_api) if senha_api else None

        success = UserModel.update(user_id, nome_completo, email, hashed_senha_api)
        if not success:
            # UserModel.update agora lança KeyError/ValueError, então este 'if not success'
            # só seria acionado se houvesse um caso em que nada foi atualizado e não houve erro.
            # No entanto, com a lógica atual de raise, ele não deve ser alcançado.
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, # Ou 422 Unprocessable Entity
                detail="Nenhum dado válido fornecido para atualização."
            )

        return get_user_by_id(user_id) # Se atualizou com sucesso, retorna o usuário atualizado

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # Conflito de dados (ex: email duplicado)
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao atualizar usuário: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao atualizar usuário: {e}"
        )


# Deleta um usuário do banco de dados pelo ID
def delete_user(user_id: int) -> bool:
    try:
        success = UserModel.delete(user_id)
        if not success: # Embora com KeyError do modelo, esta linha talvez não seja mais alcançada
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado para exclusão."
            )
        return success
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor ao excluir usuário: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado ao excluir usuário: {e}"
        )