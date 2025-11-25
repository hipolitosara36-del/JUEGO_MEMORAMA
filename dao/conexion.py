import pyodbc

class ConexionSQL:
    def __init__(self):
        self.server = "localhost"
        self.database = "memorama"
        self.username = "sa"
        self.password = "2509"

    def conectar(self):
        try:
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )

            print("Conexión establecida correctamente a SQL Server.")
            return conn

        except Exception as e:
            print("Error al conectar a SQL Server:", e)
            return None
