from datetime import datetime

class Juego:
    def __init__(self, id_sesion, nivel=1):
        self.id_sesion = id_sesion
        self.nivel = nivel
        self.cartas_volteadas = []
        self.pares_encontrados = 0
        self.tiempo_inicial = 30 + (nivel - 1) * 15
        self.tiempo_restante = self.tiempo_inicial
        self.cartas_descubiertas = []  # Posiciones de cartas ya encontradas
        self.activo = True
        self.fecha_inicio = datetime.now()

    def voltear_carta(self, posicion):
        """Registra una carta volteada"""
        if len(self.cartas_volteadas) < 2 and posicion not in self.cartas_descubiertas:
            self.cartas_volteadas.append(posicion)
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

    def juego_completado(self, total_pares):
        """Verifica si el juego está completado"""
        return self.pares_encontrados >= total_pares

    def subir_nivel(self):
        """Sube al siguiente nivel"""
        self.nivel += 1
        self.pares_encontrados = 0
        self.cartas_volteadas = []
        self.cartas_descubiertas = []
        self.tiempo_inicial = 30 + (self.nivel - 1) * 15
        self.tiempo_restante = self.tiempo_inicial
        self.activo = True

    def to_dict(self):
        """Convierte el juego a diccionario para JSON"""
        return {
            'id_sesion': self.id_sesion,
            'nivel': self.nivel,
            'pares_encontrados': self.pares_encontrados,
            'tiempo_restante': self.tiempo_restante,
            'cartas_volteadas': self.cartas_volteadas,
            'cartas_descubiertas': self.cartas_descubiertas,
            'activo': self.activo
        }