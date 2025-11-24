import random
import math

class Tablero:
    def __init__(self, total_pares, imagenes, nivel=1):
        self.total_pares_tablero = total_pares
        self.nivel = nivel  #NUEVO: Guardamos el nivel
        
        #NUEVO: Determinar si incluir carta de tiempo extra
        self.tiene_carta_tiempo = nivel >= 4
        
        # Calcular total de cartas
        if self.tiene_carta_tiempo:
            # Si hay carta de tiempo, usamos 1 par menos y agregamos 2 cartas especiales
            total_cartas = (total_pares - 1) * 2 + 2
        else:
            total_cartas = total_pares * 2
        
        # Calcular filas y columnas
        self.filas, self.columnas = self._calcular_dimensiones(total_cartas)

        # Crear el mazo de cartas
        self.cartas = self._crear_cartas(total_pares, imagenes)

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

    def _crear_cartas(self, total_pares, imagenes):
        """Crea el mazo de cartas con o sin carta de tiempo extra"""
        
        # Verificar imágenes disponibles
        if len(imagenes) < total_pares:
            print(f"⚠️ ADVERTENCIA: Solo se encontraron {len(imagenes)} imágenes. Se necesitan {total_pares}.")
            imagenes = (imagenes * (total_pares // len(imagenes) + 1))[:total_pares]
        
        if self.tiene_carta_tiempo:
            #Nivel 4+: Usar 1 par menos y agregar 2 cartas de tiempo
            pares_normales = total_pares - 1
            imagenes_a_usar = imagenes[:pares_normales]
            cartas = imagenes_a_usar * 2
            
            # Agregar 2 cartas especiales de tiempo
            cartas.extend(['imagenes/tiempo_extra.png', 'imagenes/tiempo_extra.png'])
        else:
            #Niveles 1-3: Solo pares normales
            imagenes_a_usar = imagenes[:total_pares]
            cartas = imagenes_a_usar * 2
        
        # Mezclar las cartas
        random.shuffle(cartas)
        return cartas

    def obtener_carta(self, posicion):
        """Obtiene la imagen de una carta dado su posición"""
        if 0 <= posicion < len(self.cartas):
            return self.cartas[posicion]
        return None

    def es_carta_tiempo_extra(self, carta):
        """Verifica si una carta es de tiempo extra"""
        return carta == 'imagenes/tiempo_extra.png'

    def obtener_total_pares(self):
        """Retorna el total de pares en el tablero"""
        return self.total_pares_tablero

    def to_dict(self):
        """Convierte el tablero a diccionario para JSON"""
        return {
            'filas': self.filas,
            'columnas': self.columnas,
            'total_cartas': len(self.cartas),
            'total_pares': self.total_pares_tablero,
            'tiene_carta_tiempo': self.tiene_carta_tiempo  #NUEVO
        }