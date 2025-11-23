from datetime import datetime

class Juego:
    # Definición de pares por nivel para la progresión: 2, 4, 6, 8, ...
    PARES_POR_NIVEL = {
        1: 2,  # 4 cartas (2x2)
        2: 4,  # 8 cartas (4x2)
        3: 6,  # 12 cartas (4x3)
        4: 8,  # 16 cartas (4x4)
        5: 10, # 20 cartas (5x4)
    }

    def __init__(self, id_sesion, nivel=1):
        self.id_sesion = id_sesion
        self.nivel = nivel
        self.total_pares = self.PARES_POR_NIVEL.get(nivel, 10) # Obtener el total de pares
        
        self.cartas_volteadas = []
        self.pares_encontrados = 0
        
        # --- NUEVOS CAMPOS DE PUNTUACIÓN Y TIEMPO ---
        # El tiempo se calcula según el total de pares: 10 segundos por par
        self.tiempo_inicial = self.total_pares * 10 
        self.tiempo_restante = self.tiempo_inicial
        self.movimientos = 0  # Contador de movimientos (cartas individuales volteadas)
        self.intentos_fallidos = 0 # Contador de intentos fallidos (cuando no hay pareja)
        # ---------------------------------------------

        self.cartas_descubiertas = []  # Posiciones de cartas ya encontradas
        self.activo = True
        self.fecha_inicio = datetime.now()

    def voltear_carta(self, posicion):
        """Registra una carta volteada e incrementa los movimientos"""
        if len(self.cartas_volteadas) < 2 and posicion not in self.cartas_descubiertas:
            self.cartas_volteadas.append(posicion)
            self.movimientos += 1  # Incrementa el conteo de movimientos
            return True
        return False

    def verificar_pareja(self, carta1, carta2):
        """Verifica si dos cartas son pareja"""
        if carta1 == carta2:
            self.pares_encontrados += 1
            # Agregar las posiciones a las cartas descubiertas
            self.cartas_descubiertas.extend(self.cartas_volteadas)
            self.cartas_volteadas = []
            return True
        else:
            self.intentos_fallidos += 1 # Aumenta el contador de intentos fallidos
            self.cartas_volteadas = []
            return False

    def reducir_tiempo(self):
        """Reduce el tiempo en 1 segundo"""
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return True
        else:
            self.activo = False
            return False

    def juego_completado(self):
        """Verifica si el juego está completado. Usa self.total_pares"""
        return self.pares_encontrados >= self.total_pares

    def subir_nivel(self):
        """Sube al siguiente nivel, reestableciendo el estado con nuevos parámetros"""
        siguiente_nivel = self.nivel + 1
        
        if siguiente_nivel in self.PARES_POR_NIVEL:
            self.nivel = siguiente_nivel
            self.total_pares = self.PARES_POR_NIVEL[self.nivel]
            
            # Resetear el estado del juego
            self.pares_encontrados = 0
            self.cartas_volteadas = []
            self.cartas_descubiertas = []
            self.movimientos = 0
            self.intentos_fallidos = 0
            
            # Nuevo tiempo basado en los nuevos pares
            self.tiempo_inicial = self.total_pares * 10
            self.tiempo_restante = self.tiempo_inicial
            self.activo = True
            return True
        return False # No hay más niveles definidos

    def to_dict(self):
        """Convierte el juego a diccionario para JSON"""
        return {
            'id_sesion': self.id_sesion,
            'nivel': self.nivel,
            'total_pares': self.total_pares,
            'pares_encontrados': self.pares_encontrados,
            'tiempo_restante': self.tiempo_restante,
            'tiempo_inicial': self.tiempo_inicial,
            'movimientos': self.movimientos,
            'intentos_fallidos': self.intentos_fallidos,
            'cartas_volteadas': self.cartas_volteadas,
            'cartas_descubiertas': self.cartas_descubiertas,
            'activo': self.activo
        }