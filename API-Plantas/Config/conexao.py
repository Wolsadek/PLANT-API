import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def obter_conexao():
    """Cria e devolve uma nova conexão com o MySQL do XAMPP."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "api_plantas"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        charset="utf8mb4",
    )

