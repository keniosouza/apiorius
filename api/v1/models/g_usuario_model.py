# models/g_usuario_model.py

from firebird.driver.types import DatabaseError # Importe esta exceção específica
from core.database import get_connection
# Se você tiver core.configs, pode ser útil para logs ou configurações
# from core.configs import settings

class UserModel:
    """
    Classe responsável por interagir diretamente com o banco de dados Firebird.
    Nenhuma validação ou sanitização deve ser feita aqui.
    """

    @staticmethod
    def get_by_email(email: str) -> dict | None:
        """
        Retorna um usuário com base no e-mail, ou None se não encontrado.
        Lança exceções em caso de falha no banco de dados.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT USUARIO_ID, EMAIL, SENHA_API, NOME_COMPLETO
                FROM G_USUARIO
                WHERE EMAIL = ?
            """, (email,))
            row = cur.fetchone()

            if row:
                return {
                    "user_id": row[0],
                    "email": row[1],
                    "senha_api": row[2],
                    "nome_completo": row[3],
                }
            return None
        except DatabaseError as e:
            # Erros específicos do Firebird (ex: problema na conexão, query inválida)
            print(f"Database error in get_by_email: {e}")
            raise RuntimeError(f"Erro ao buscar usuário por e-mail no banco de dados: {e}")
        except Exception as e:
            # Qualquer outro erro inesperado
            print(f"Unexpected error in get_by_email: {e}")
            raise RuntimeError(f"Erro inesperado ao buscar usuário por e-mail: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(user_id: int) -> dict | None:
        """
        Retorna um usuário com base no ID, ou None se não encontrado.
        Lança exceções em caso de falha no banco de dados.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT USUARIO_ID, 
                       NOME_COMPLETO, 
                       EMAIL,
                       TELEFONE
                FROM G_USUARIO
                WHERE USUARIO_ID = ?
            """, (user_id,))
            row = cur.fetchone()

            if row:
                return {
                    "user_id": row[0],
                    "nome_completo": row[1],
                    "email": row[2],
                    "telefone": row[3],
                }
            return None
        except DatabaseError as e:
            print(f"Database error in get_by_id: {e}")
            raise RuntimeError(f"Erro ao buscar usuário por ID no banco de dados: {e}")
        except Exception as e:
            print(f"Unexpected error in get_by_id: {e}")
            raise RuntimeError(f"Erro inesperado ao buscar usuário por ID: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def count_users() -> int:
        """
        Retorna a quantidade de usuários.
        """        
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM G_USUARIO")
            total = cur.fetchone()[0]
            return total
        except Exception as e:
            raise RuntimeError(f"Erro ao contar usuários: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()     


    @staticmethod
    def get_all(skip: int = 0, limit: int = 10) -> list[dict]:
        """
        Retorna todos os usuários cadastrados no banco de dados.
        Lança exceções em caso de falha no banco de dados.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            query = f"""
                SELECT FIRST {limit} SKIP {skip}
                    USUARIO_ID, 
                    TROCARSENHA, 
                    LOGIN, 
                    SITUACAO, 
                    NOME_COMPLETO, 
                    FUNCAO,
                    ASSINA, 
                    SIGLA, 
                    USUARIO_TAB, 
                    ULTIMO_LOGIN, 
                    ULTIMO_LOGIN_REGS,
                    DATA_EXPIRACAO,
                    ANDAMENTO_PADRAO, 
                    LEMBRETE_PERGUNTA, 
                    LEMBRETE_RESPOSTA,
                    ANDAMENTO_PADRAO2, 
                    RECEBER_MENSAGEM_ARROLAMENTO, 
                    EMAIL, 
                    ASSINA_CERTIDAO,
                    RECEBER_EMAIL_PENHORA, 
                    FOTO, 
                    NAO_RECEBER_CHAT_TODOS, 
                    PODE_ALTERAR_CAIXA,
                    RECEBER_CHAT_CERTIDAO_ONLINE, 
                    RECEBER_CHAT_CANCELAMENTO, 
                    CPF, 
                    SOMENTE_LEITURA,
                    RECEBER_CHAT_ENVIO_ONR, 
                    TIPO_USUARIO, 
                    DATA_CADASTRO
                FROM G_USUARIO
                ORDER BY USUARIO_ID
            """           

            cur.execute(query)
            rows = cur.fetchall()

            return [
                {
                    "usuario_id": r[0],
                    "trocarsenha": r[1],
                    "login": r[2],
                    "situacao": r[3],
                    "nome_completo": r[4],
                    "funcao": r[5],
                    "assina": r[6],
                    "sigla": r[7],
                    "usuario_tab": r[8],
                    "ultimo_login": r[9],
                    "ultimo_login_regs": r[10],
                    "data_expiracao": r[11],
                    "andamento_padrao": r[12],
                    "lembrete_pergunta": r[13],
                    "lembrete_resposta": r[14],
                    "andamento_padrao2": r[15],
                    "receber_mensagem_arrolamento": r[16],
                    "email": r[17],
                    "assina_certidao": r[18],
                    "receber_email_penhora": r[19],
                    "foto": r[20],
                    "nao_receber_chat_todos": r[21],
                    "pode_alterar_caixa": r[22],
                    "receber_chat_certidao_online": r[23],
                    "receber_chat_cancelamento": r[24],
                    "cpf": r[25],
                    "somente_leitura": r[26],
                    "receber_chat_envio_onr": r[27],
                    "tipo_usuario": r[28],
                    "data_cadastro": r[29],
                    "telefone": r[30],
                }
                for r in rows
            ]
        except DatabaseError as e:
            print(f"Database error in get_all: {e}")
            raise RuntimeError(f"Erro ao buscar todos os usuários no banco de dados: {e}")
        except Exception as e:
            print(f"Unexpected error in get_all: {e}")
            raise RuntimeError(f"Erro inesperado ao buscar todos os usuários: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def create(nome_completo: str, email: str, senha_api: str) -> dict | None:
        """
        Cria um novo usuário no banco. Lança exceções para e-mail duplicado
        ou outros erros de banco de dados.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            # A validação de e-mail duplicado feita aqui no modelo é um pouco redundante
            # se você já tiver uma UNIQUE constraint no EMAIL.
            # O tratamento de exceção abaixo (DatabaseError) já capturaria a violação da UNIQUE constraint.
            # No entanto, se você não tiver uma constraint UNIQUE, esta verificação é válida.
            # Se tiver uma constraint, pode remover este SELECT e deixar o DB lançar o erro.
            cur.execute("SELECT 1 FROM G_USUARIO WHERE EMAIL = ?", (email,))
            if cur.fetchone():
                # Captura de um e-mail já existente antes de tentar a inserção
                # Isso evita um DatabaseError mais tarde e permite uma mensagem mais específica.
                raise ValueError("E-mail já cadastrado. Por favor, use outro e-mail.")

            cur.execute("""
                INSERT INTO G_USUARIO (NOME_COMPLETO, EMAIL, SENHA_API)
                VALUES (?, ?, ?)
                RETURNING USUARIO_ID
            """, (nome_completo, email, senha_api))

            user_id = cur.fetchone()[0]
            conn.commit()

            return {
                "user_id": user_id,
                "nome_completo": nome_completo,
                "email": email,
            }
        except DatabaseError as e:
            if conn:
                conn.rollback() # Desfaz a transação em caso de erro no DB
            error_message = str(e).lower()
            # Tratamento específico para violação de UNIQUE KEY ou PRIMARY KEY
            if "violation of primary or unique key constraint" in error_message or "duplicate value" in error_message:
                # Se você tem certeza de que USUARIO_ID e EMAIL são as únicas chaves únicas/primárias
                # e o EMAIL já foi verificado acima, então este erro aponta para USUARIO_ID.
                # No entanto, é mais robusto verificar o nome da constraint se possível, ou ser mais genérico.
                if "g_usuario_pk" in error_message: # Supondo que G_USUARIO_PK é para USUARIO_ID
                     raise ValueError(f"O ID gerado para o usuário já existe. Tente novamente ou verifique os dados: {error_message}")
                # Se você tiver uma constraint UNIQUE no EMAIL, isso também seria capturado aqui
                elif "seu_email_unique_constraint_name" in error_message: # Substitua pelo nome real da sua constraint de email
                    raise ValueError(f"Já existe um usuário com este e-mail: {email}. Erro: {error_message}")
                else: # Outras violações de chaves únicas
                    raise ValueError(f"Violação de restrição de dados. Verifique os campos fornecidos. Detalhe: {error_message}")
            else:
                # Outros erros de DatabaseError
                raise RuntimeError(f"Erro no banco de dados ao criar usuário: {error_message}")
        except ValueError as e:
            # Re-lança o ValueError de e-mail duplicado, se a verificação acima estiver ativa
            raise e
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Unexpected error in create: {e}")
            raise RuntimeError(f"Erro inesperado ao criar usuário: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def update(user_id: int, nome_completo: str | None, email: str | None, senha_api: str | None, telefone: str | None) -> bool:
        """
        Atualiza os dados de um usuário existente.
        Lança exceções se o usuário não for encontrado ou em caso de erro no DB.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Verifica se o usuário existe antes de tentar atualizar
            cur.execute("SELECT 1 FROM G_USUARIO WHERE USUARIO_ID = ?", (user_id,))
            if not cur.fetchone():
                raise KeyError(f"Usuário com ID {user_id} não encontrado para atualização.")

            updates = []
            params = []

            if nome_completo is not None:
                updates.append("NOME_COMPLETO = ?")
                params.append(nome_completo)
            if email is not None:
                # Verifique se o novo e-mail já existe para outro usuário (se email for uma chave única)
                cur.execute("SELECT USUARIO_ID FROM G_USUARIO WHERE EMAIL = ? AND USUARIO_ID <> ?", (email, user_id))
                if cur.fetchone():
                    raise ValueError(f"O e-mail '{email}' já está sendo usado por outro usuário.")
                updates.append("EMAIL = ?")
                params.append(email)
            if senha_api is not None:
                updates.append("SENHA_API = ?")
                params.append(senha_api)
            if telefone is not None:
                updates.append("TELEFONE = ?")
                params.append(telefone)                

            if not updates: # Se nenhum campo foi fornecido para atualização
                return False

            query = f"UPDATE G_USUARIO SET {', '.join(updates)} WHERE USUARIO_ID = ?"
            params.append(user_id)

            cur.execute(query, tuple(params))
            conn.commit()

            return True
        except DatabaseError as e:
            if conn:
                conn.rollback()
            error_message = str(e).lower()
            if "violation of unique constraint" in error_message or "duplicate value" in error_message:
                # Captura violação de unique constraint no email, se houver
                raise ValueError(f"Erro de dados duplicados ao atualizar: {error_message}")
            else:
                raise RuntimeError(f"Erro no banco de dados ao atualizar usuário: {e}")
        except (KeyError, ValueError) as e:
            # Re-lança as exceções de não encontrado ou e-mail duplicado
            raise e
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Unexpected error in update: {e}")
            raise RuntimeError(f"Erro inesperado ao atualizar usuário: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def delete(user_id: int) -> bool:
        """
        Exclui um usuário com base no ID. Lança exceção se o usuário não for encontrado.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Verifica se o usuário existe antes de tentar deletar
            cur.execute("SELECT 1 FROM G_USUARIO WHERE USUARIO_ID = ?", (user_id,))
            if not cur.fetchone():
                raise KeyError(f"Usuário com ID {user_id} não encontrado para exclusão.")

            cur.execute("DELETE FROM G_USUARIO WHERE USUARIO_ID = ?", (user_id,))
            conn.commit()

            return True
        except DatabaseError as e:
            if conn:
                conn.rollback()
            print(f"Database error in delete: {e}")
            raise RuntimeError(f"Erro no banco de dados ao excluir usuário: {e}")
        except KeyError as e:
            # Re-lança a exceção de não encontrado
            raise e
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Unexpected error in delete: {e}")
            raise RuntimeError(f"Erro inesperado ao excluir usuário: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()