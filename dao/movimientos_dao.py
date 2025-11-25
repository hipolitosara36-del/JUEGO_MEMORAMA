from dao.conexion import ConexionSQL

class MovimientosDAO:
    def __init__(self):
        self.conexion = ConexionSQL()

    def registrar_movimiento(self, id_sesion, accion, posicion=None):
        conn = self.conexion.conectar()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Movimientos (id_sesion, accion, posicion)
                VALUES (?, ?, ?)
            """, (id_sesion, accion, posicion))

            conn.commit()
            return True

        except Exception as e:
            print("Error al registrar movimiento:", e)
            return False

        finally:
            conn.close()


