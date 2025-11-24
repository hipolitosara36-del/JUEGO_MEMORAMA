import os
from models.juego import Juego
from models.tablero import Tablero

# Diccionarios de almacenamiento temporal (simulando persistencia)
JUEGOS_ACTIVOS = {}
TABLEROS_ACTIVOS = {}
      
# Ruta correcta de imágenes (relativa a la carpeta static)
IMAGENES_DISPONIBLES = [f"imagenes/{i}.png" for i in range(1, 48)]

class JuegoDAO:
    def __init__(self):
        pass

    def crear_juego(self, id_sesion, nivel=1):
        """Crea un nuevo juego y tablero para la sesión dada."""
        
        # 1. Crear el objeto Juego
        juego = Juego(id_sesion, nivel)
        
        # 2. Crear el objeto Tablero
        total_pares = juego.total_pares
        tablero = Tablero(total_pares, IMAGENES_DISPONIBLES)
        
        print(f"🔍 Creando juego - Nivel: {nivel}")
        print(f"🔍 Total pares: {total_pares}")
        print(f"🔍 Tiene carta tiempo: {tablero.tiene_carta_tiempo}")
        print(f"🔍 Total cartas en tablero: {len(tablero.cartas)}")
        print(f"🔍 Primeras 5 cartas: {tablero.cartas[:5]}")
        
        # 3. Guardar en "base de datos" (diccionario en memoria)
        JUEGOS_ACTIVOS[id_sesion] = juego
        TABLEROS_ACTIVOS[id_sesion] = tablero
        
        return juego

    def obtener_juego(self, id_sesion):
        """Obtiene el objeto Juego de la sesión."""
        return JUEGOS_ACTIVOS.get(id_sesion)

    def obtener_tablero(self, id_sesion):
        """Obtiene el objeto Tablero de la sesión."""
        return TABLEROS_ACTIVOS.get(id_sesion)

    def voltear_carta(self, id_sesion, posicion):
        """
        Voltea una carta y retorna su imagen.
        Si ya hay 2 cartas volteadas, retorna None (esperar verificación).
        """
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero:
            return None
        
        # Verificar si se puede voltear
        if juego.voltear_carta(posicion):
            return tablero.obtener_carta(posicion)
        
        return None

    def verificar_pareja(self, id_sesion):
        """
        Verifica si las 2 cartas volteadas son pareja.
        Retorna diccionario con resultado.
        """
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero:
            return None
        
        if len(juego.cartas_volteadas) != 2:
            return None
        
        # Obtener las cartas
        pos1, pos2 = juego.cartas_volteadas
        carta1 = tablero.obtener_carta(pos1)
        carta2 = tablero.obtener_carta(pos2)
        
        # Verificar pareja
        es_pareja = juego.verificar_pareja(carta1, carta2)
        
        return {
            'es_pareja': es_pareja,
            'juego_completado': juego.juego_completado()
        }

    def reiniciar_juego(self, id_sesion):
        """Reinicia el juego actual (mismo nivel)"""
        juego = self.obtener_juego(id_sesion)
        if juego:
            nivel_actual = juego.nivel
            return self.crear_juego(id_sesion, nivel_actual)
        return None

    def subir_nivel(self, id_sesion):
        """Sube al siguiente nivel y retorna el juego actualizado"""
        juego = self.obtener_juego(id_sesion)
        if juego and juego.subir_nivel():
            # Crear nuevo tablero con el nuevo total de pares
            tablero = Tablero(juego.total_pares, IMAGENES_DISPONIBLES)
            TABLEROS_ACTIVOS[id_sesion] = tablero
            return juego
        return None

    def reducir_tiempo(self, id_sesion):
        """Reduce el tiempo del juego en 1 segundo"""
        juego = self.obtener_juego(id_sesion)
        if juego:
            juego.reducir_tiempo()
            return juego
        return None

    def obtener_estado_juego(self, id_sesion):
        """Obtiene el estado completo del juego"""
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero:
            return None
        
        return {
            **juego.to_dict(),
            'tablero': tablero.to_dict()
        }