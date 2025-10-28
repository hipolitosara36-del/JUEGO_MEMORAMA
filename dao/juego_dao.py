import os
from models.juego import Juego
from models.tablero import Tablero

class JuegoDAO:
    """DAO para gestionar el estado de los juegos en memoria"""
    
    def __init__(self):
        self.juegos = {}  # Almacena juegos por id_sesion
        self.tableros = {}  # Almacena tableros por id_sesion
        self.imagenes = self.cargar_imagenes()

    def cargar_imagenes(self):
        """Carga las rutas de las imágenes disponibles"""
        ruta = "static/imagenes"
        imagenes = []
        
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            
        for archivo in os.listdir(ruta):
            if archivo.endswith((".png", ".jpg", ".jpeg")) and archivo != "interrogacion.png":
                imagenes.append(f"/static/imagenes/{archivo}")
        
        return imagenes

    def crear_juego(self, id_sesion, nivel=1):
        """Crea un nuevo juego"""
        juego = Juego(id_sesion, nivel)
        self.juegos[id_sesion] = juego
        
        # Crear tablero
        filas = columnas = 2 * nivel
        tablero = Tablero(filas, columnas, self.imagenes)
        self.tableros[id_sesion] = tablero
        
        return juego

    def obtener_juego(self, id_sesion):
        """Obtiene un juego existente"""
        return self.juegos.get(id_sesion)

    def obtener_tablero(self, id_sesion):
        """Obtiene el tablero de un juego"""
        return self.tableros.get(id_sesion)

    def actualizar_juego(self, id_sesion, juego):
        """Actualiza el estado de un juego"""
        self.juegos[id_sesion] = juego
        return juego

    def voltear_carta(self, id_sesion, posicion):
        """Registra el volteo de una carta"""
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero:
            return None
        
        if juego.voltear_carta(posicion):
            carta = tablero.obtener_carta(posicion)
            return carta
        return None

    def verificar_pareja(self, id_sesion):
        """Verifica si las cartas volteadas son pareja"""
        juego = self.obtener_juego(id_sesion)
        tablero = self.obtener_tablero(id_sesion)
        
        if not juego or not tablero or len(juego.cartas_volteadas) != 2:
            return None
        
        pos1, pos2 = juego.cartas_volteadas
        carta1 = tablero.obtener_carta(pos1)
        carta2 = tablero.obtener_carta(pos2)
        
        es_pareja = juego.verificar_pareja(carta1, carta2)
        juego_completado = juego.juego_completado(tablero.total_pares())
        
        return {
            'es_pareja': es_pareja,
            'juego_completado': juego_completado
        }

    def subir_nivel(self, id_sesion):
        """Sube el juego al siguiente nivel"""
        juego = self.obtener_juego(id_sesion)
        if juego:
            juego.subir_nivel()
            # Crear nuevo tablero para el nuevo nivel
            filas = columnas = 2 * juego.nivel
            tablero = Tablero(filas, columnas, self.imagenes)
            self.tableros[id_sesion] = tablero
            return juego
        return None

    def reducir_tiempo(self, id_sesion):
        """Reduce el tiempo del juego"""
        juego = self.obtener_juego(id_sesion)
        if juego:
            juego.reducir_tiempo()
            return juego
        return None

    def eliminar_juego(self, id_sesion):
        """Elimina un juego de la memoria"""
        if id_sesion in self.juegos:
            del self.juegos[id_sesion]
        if id_sesion in self.tableros:
            del self.tableros[id_sesion]