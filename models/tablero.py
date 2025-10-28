import random

class Tablero:
    def __init__(self, filas, columnas, imagenes):
        self.filas = filas
        self.columnas = columnas
        total_cartas = filas * columnas

        # Seleccionar solo las imágenes necesarias
        imagenes = imagenes[:total_cartas // 2]
        cartas = imagenes * 2
        random.shuffle(cartas)

        self.cartas = cartas

    def obtener_carta(self, posicion):
        """Obtiene la imagen de una carta dado su posición"""
        if 0 <= posicion < len(self.cartas):
            return self.cartas[posicion]
        return None

    def total_pares(self):
        """Retorna el total de pares en el tablero"""
        return len(self.cartas) // 2

    def to_dict(self):
        """Convierte el tablero a diccionario para JSON"""
        return {
            'filas': self.filas,
            'columnas': self.columnas,
            'total_cartas': len(self.cartas)
        }