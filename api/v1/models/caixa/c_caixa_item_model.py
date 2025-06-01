# models/c_caixa_item_model.py

from firebird.driver.types import DatabaseError # Importe esta exceção específica
from core.database import get_connection
# Se você tiver core.configs, pode ser útil para logs ou configurações
# from core.configs import settings

class CCaixaItemModel:
    """
    Classe responsável por interagir diretamente com o banco de dados Firebird.
    Nenhuma validação ou sanitização deve ser feita aqui.
    """

    @staticmethod
    def get_by_id(caixa_item_id: int) -> dict | None:
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
                SELECT CAIXA_ITEM_ID,
                       DESCRICAO,
                       DATA_PAGAMENTO,
                       VALOR_SERVICO,
                       VALOR_PAGO,
                       APRESENTANTE
                FROM C_CAIXA_ITEM
                WHERE CAIXA_ITEM_ID = ?
            """, (caixa_item_id,))
            row = cur.fetchone()

            if row:
                return {
                    "caixa_item_id": row[0],
                    "descricao": row[1],
                    "data_pagamento": row[2],
                    "valor_servico": row[3],
                    "valor_pago": row[4],
                    "apresentante": row[5],
                }
            return None
        except DatabaseError as e:
            print(f"Database error in get_by_id: {e}")
            raise RuntimeError(f"Erro ao buscar item por ID no banco de dados: {e}")
        except Exception as e:
            print(f"Unexpected error in get_by_id: {e}")
            raise RuntimeError(f"Erro inesperado ao buscar item por ID: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def count_items() -> int:
        """
        Retorna a quantidade de usuários.
        """        
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM C_CAIXA_ITEM")
            total = cur.fetchone()[0]
            return total
        except Exception as e:
            raise RuntimeError(f"Erro ao contar itens: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()     


    @staticmethod
    def get_all_caixa_itens(skip: int = 0, limit: int = 10) -> list[dict]:
        """
        Retorna todos os itens cadastrados no banco de dados.
        Lança exceções em caso de falha no banco de dados.
        """
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            query = f"""
                SELECT FIRST {limit} SKIP {skip}
                    CAIXA_ITEM_ID,
                       DESCRICAO,
                       DATA_PAGAMENTO,
                       VALOR_SERVICO,
                       VALOR_PAGO,
                       APRESENTANTE
                FROM C_CAIXA_ITEM
                ORDER BY CAIXA_ITEM_ID
            """           

            cur.execute(query)
            rows = cur.fetchall()

            return [
                {
                    "caixa_item_id": r[0],
                    "descricao": r[1],
                    "data_pagamento": r[2],
                    "valor_servico": r[3],
                    "valor_pago": r[4],
                    "apresentante": r[5],
                }
                for r in rows
            ]
        except DatabaseError as e:
            print(f"Database error in get_all: {e}")
            raise RuntimeError(f"Erro ao buscar todos os itens no banco de dados: {e}")
        except Exception as e:
            print(f"Unexpected error in get_all: {e}")
            raise RuntimeError(f"Erro inesperado ao buscar todos os itens: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()    