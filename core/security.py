# core/security.py

# Importa CryptContext da biblioteca passlib para operações de hash de senha
from passlib.context import CryptContext

# Cria uma instância do contexto de criptografia
# O esquema usado é 'bcrypt', que é seguro e amplamente aceito
# O parâmetro 'deprecated="auto"' marca versões antigas como inseguras, se aplicável
CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Verifica se uma senha fornecida corresponde ao hash armazenado
def verify_senha_api(plain_senha_api: str, hashed_senha_api: str) -> bool:
    """
    Compara a senha fornecida em texto puro com o hash armazenado.
    
    :param plain_senha_api: Senha digitada pelo usuário
    :param hashed_senha_api: Hash da senha armazenado no banco de dados
    :return: True se corresponder, False se não
    """
    return CRYPTO.verify(plain_senha_api, hashed_senha_api)


# Gera o hash de uma senha fornecida
def hash_senha_api(plain_senha_api: str) -> str:
    """
    Gera e retorna o hash da senha fornecida.

    :param plain_senha_api: Senha em texto puro fornecida pelo usuário
    :return: Hash da senha
    """
    return CRYPTO.hash(plain_senha_api)
