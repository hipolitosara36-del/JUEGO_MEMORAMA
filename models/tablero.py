import random
import math

class Tablero:
    def __init__(self, total_pares, imagenes):
        self.total_pares = total_pares
        total_cartas = total_pares * 2
        
        # Calcular filas y columnas (cuadrado o rectangular cercano)
        self.filas, self.columnas = self._calcular_dimensiones(total_cartas)

        # Seleccionar solo las imágenes necesarias
        # Asegurarse de tener suficientes imágenes disponibles
        if len(imagenes) < total_pares:
            print(f"ADVERTENCIA: Solo se encontraron {len(imagenes)} imágenes. Se necesitan {total_pares}.")
            imagenes = (imagenes * (total_pares // len(imagenes) + 1))[:total_pares]

        imagenes_a_usar = imagenes[:total_pares]
        cartas = imagenes_a_usar * 2
        random.shuffle(cartas)

        self.cartas = cartas

    def _calcular_dimensiones(self, total_cartas):
        """
        Calcula las dimensiones (filas, columnas) para el tablero.
        Intenta mantener una proporción cuadrada (N x M, donde N ~ M).
        """
        if total_cartas == 0:
            return 0, 0
            
        # Calcula la raíz cuadrada entera
        c = int(math.sqrt(total_cartas)) 
        
        # Busca el factor más cercano a la raíz cuadrada
        filas = 1
        for i in range(c, 0, -1):
            if total_cartas % i == 0:
                filas = i
                break
        
        columnas = total_cartas // filas
        return filas, columnas

    def obtener_carta(self, posicion):
        """Obtiene la imagen de una carta dado su posición"""
        if 0 <= posicion < len(self.cartas):
            return self.cartas[posicion]
        return None

    def total_pares(self):
        """Retorna el total de pares en el tablero (ya lo tenemos en self.total_pares)"""
        return self.total_pares

    def to_dict(self):
        """Convierte el tablero a diccionario para JSON"""
        return {
            'filas': self.filas,
            'columnas': self.columnas,
            'total_cartas': len(self.cartas),
            'total_pares': self.total_pares
        }