import pyodbc

def get_connection():
    server = 'localhost'         # O tu IP/instancia
    database = 'memorama'        # Cambia al nombre de tu BD
    username = 'sa'              # Tu usuario
    password = '2509'     # Tu contraseña
    driver = '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )

    return conn

