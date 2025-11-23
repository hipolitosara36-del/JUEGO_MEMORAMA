import os
from .models.juego import Juego
from .models.tablero import Tablero

# Diccionarios de almacenamiento temporal (simulando persistencia)
JUEGOS_ACTIVOS = {}
TABLEROS_ACTIVOS = {}

# Lista de imágenes disponibles (ejemplo, debes adaptarla a tus archivos)
# Asume que tienes 10 imágenes: img_1.png, img_2.png, ..., img_10.png
IMAGENES_DISPONIBLES = [f'img_{i}.png' for i in range(1, 11)]

class JuegoDAO:
    def __init__(self):
        pass

    def crear_juego(self, id_sesion, nivel=1):
        """Crea un nuevo juego y tablero para la sesión dada."""
        
        # 1. Crear el objeto Juego, que determina el total_pares
        juego = Juego(id_sesion, nivel)
        
        # 2. Crear el objeto Tablero, que usa el total_pares del juego
        total_pares = juego.total_pares
        tablero = Tablero(total_pares, IMAGENES_DISPONIBLES)
        
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
        """Maneja la lógica de voltear una carta y retorna su valor."""
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero or not juego.activo:
            return None # El juego no está activo o no existe
        
        if juego.voltear_carta(posicion):
            return tablero.obtener_carta(posicion)
        
        return None

    def verificar_pareja(self, id_sesion):
        """Verifica si las cartas volteadas son pareja."""
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero or len(juego.cartas_volteadas) != 2:
            return None

        # Obtener los valores de las dos cartas volteadas
        pos1, pos2 = juego.cartas_volteadas
        carta1_valor = tablero.obtener_carta(pos1)
        carta2_valor = tablero.obtener_carta(pos2)
        
        es_pareja = juego.verificar_pareja(carta1_valor, carta2_valor)
        juego_completado = juego.juego_completado()
        
        return {
            'es_pareja': es_pareja,
            'juego_completado': juego_completado
        }

    def subir_nivel(self, id_sesion):
        """Llama a la lógica de subir nivel y crea el nuevo tablero."""
        juego = self.obtener_juego(id_sesion)
        if juego and juego.subir_nivel():
            # Crear el nuevo tablero para el nuevo nivel
            total_pares = juego.total_pares
            tablero = Tablero(total_pares, IMAGENES_DISPONIBLES)
            TABLEROS_ACTIVOS[id_sesion] = tablero
            return juego
        return None

    def reducir_tiempo(self, id_sesion):
        """Reduce el tiempo del juego."""
        juego = self.obtener_juego(id_sesion)
        if juego and juego.activo:
            juego.reducir_tiempo()
            return juego
        return None