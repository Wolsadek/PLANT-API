from Config.conexao import obter_conexao


class Planta:
    """Model responsável pelas operações da tabela plural `plantas`."""

    tabela = "plantas"

    @classmethod
    def consultar_todas(cls):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute(f"SELECT * FROM {cls.tabela} ORDER BY id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def consultar_por_id(cls, planta_id):
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute(
                f"SELECT * FROM {cls.tabela} WHERE id = %s",
                (planta_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def cadastrar(cls, dados):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            sql = f"""
                INSERT INTO {cls.tabela}
                    (nome_popular, nome_cientifico, tipo,
                     necessidade_luz, frequencia_rega_dias, toxica)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (
                dados["nome_popular"],
                dados["nome_cientifico"],
                dados["tipo"],
                dados["necessidade_luz"],
                dados["frequencia_rega_dias"],
                dados["toxica"],
            )
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.lastrowid
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def atualizar(cls, planta_id, dados):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            sql = f"""
                UPDATE {cls.tabela}
                SET nome_popular = %s,
                    nome_cientifico = %s,
                    tipo = %s,
                    necessidade_luz = %s,
                    frequencia_rega_dias = %s,
                    toxica = %s
                WHERE id = %s
            """
            valores = (
                dados["nome_popular"],
                dados["nome_cientifico"],
                dados["tipo"],
                dados["necessidade_luz"],
                dados["frequencia_rega_dias"],
                dados["toxica"],
                planta_id,
            )
            cursor.execute(sql, valores)
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

    @classmethod
    def excluir(cls, planta_id):
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                f"DELETE FROM {cls.tabela} WHERE id = %s",
                (planta_id,),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except Exception:
            conexao.rollback()
            raise
        finally:
            cursor.close()
            conexao.close()

