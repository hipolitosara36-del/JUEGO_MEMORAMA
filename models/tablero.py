import random
import math

class Tablero:
    def __init__(self, total_pares, imagenes, nivel=1):
        self.total_pares_tablero = total_pares
        self.nivel = nivel
        
        # A partir del nivel 4 aparece la carta especial
        self.tiene_carta_tiempo = nivel >= 4
        
        # Calcular total de cartas
        if self.tiene_carta_tiempo:
            # Un par normal menos, y se agrega el par especial
            total_cartas = (total_pares - 1) * 2 + 2
        else:
            total_cartas = total_pares * 2
        
        # Calcular filas y columnas
        self.filas, self.columnas = self._calcular_dimensiones(total_cartas)

        # Crear el mazo
        self.cartas = self._crear_cartas(total_pares, imagenes)

    def _calcular_dimensiones(self, total_cartas):
        if total_cartas == 0:
            return 0, 0
            
        c = int(math.sqrt(total_cartas)) 
        filas = 1
        for i in range(c, 0, -1):
            if total_cartas % i == 0:
                filas = i
                break
        
        columnas = total_cartas // filas
        return filas, columnas

    def _crear_cartas(self, total_pares, imagenes):
        # Verificación de imágenes suficientes
        if len(imagenes) < total_pares:
            print(f"⚠️ ADVERTENCIA: Solo {len(imagenes)} imágenes. Se necesitan {total_pares}.")
            imagenes = (imagenes * (total_pares // len(imagenes) + 1))[:total_pares]
        
        # Si hay carta especial
        if self.tiene_carta_tiempo:
            pares_normales = total_pares - 1
            imagenes_normales = imagenes[:pares_normales]

            cartas = []

            # Agregar pares normales
            cartas.extend(imagenes_normales * 2)

            # Agregar el par especial de tiempo
            cartas.append("tiempo_extra") 
            cartas.append("tiempo_extra")
        else:
            # Sin carta especial
            imagenes_normales = imagenes[:total_pares]
            cartas = imagenes_normales * 2
        
        random.shuffle(cartas)
        return cartas

    def obtener_carta(self, posicion):
        if 0 <= posicion < len(self.cartas):
            return self.cartas[posicion]
        return None

    def es_carta_tiempo_extra(self, carta):
        return carta == "tiempo_extra"

    def mensaje_carta_tiempo(self):
        return "¡Carta de tiempo! Encuentra su pareja para ganar segundos extra."

    def obtener_total_pares(self):
        return self.total_pares_tablero

    def to_dict(self):
        return {
            'filas': self.filas,
            'columnas': self.columnas,
            'total_cartas': len(self.cartas),
            'total_pares': self.total_pares_tablero,
            'tiene_carta_tiempo': self.tiene_carta_tiempo
        }
