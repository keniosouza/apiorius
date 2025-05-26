import os
from urllib.parse import urlparse, unquote
from firebird.driver import connect
from core.configs import settings

def get_connection():
    parsed = urlparse(settings.DB_URL)

    user = parsed.username
    password = unquote(parsed.password or '')
    host = parsed.hostname
    port = parsed.port or 3050
    database = parsed.path.lstrip('/')

    # Ajusta o caminho no Windows: transforma '/' em '\'
    if os.name == 'nt':  # 'nt' = Windows
        database = database.replace('/', '\\')

    # Constrói o DSN no formato 'hostname/port:database_path'
    # E essa string é passada como o PRIMEIRO ARGUMENTO POSICIONAL
    connection_dsn = f"{host}/{port}:{database}"

    return connect(
        connection_dsn, # Este é o DSN completo que o driver espera
        user=user,
        password=password,
        charset="UTF8"
    )