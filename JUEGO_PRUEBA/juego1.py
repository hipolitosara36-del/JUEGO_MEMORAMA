import tkinter as tk
import random
from tkinter import messagebox

# ========================
# Clase Carta
# ========================

class Carta:
    def __init__(self, simbolo):
        self.__simbolo = simbolo
        self.__visible = False
        self.__emparejada = False

    def voltear(self):
        if not self.__emparejada:
            self.__visible = not self.__visible

    def mostrar(self):
        if self.__visible or self.__emparejada:
            return self.__simbolo
        return "❓"

    def es_igual(self, otra_carta):
        return self.__simbolo == otra_carta.__simbolo

    def emparejar(self):
        self.__emparejada = True

    def esta_emparejada(self):
        return self.__emparejada

    def get_simbolo(self):
        return self.__simbolo


# ========================
# Clase Jugador
# ========================
class Jugador:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__puntaje = 0
        self.nivel = 1

    def aumentar_puntaje(self):
        self.__puntaje += 1

    def get_puntaje(self):
        return self.__puntaje

    def get_nombre(self):
        return self.__nombre

    def subir_nivel(self):
        self.nivel += 1


# ========================
# Clase Tablero
# ========================
class Tablero:
    def __init__(self, filas=4, columnas=4, incluir_especial=True):
        simbolos = list("ABCDEFGH") * 2
        if incluir_especial:
            simbolos.append("⏰")
            simbolos.append("⏰")

        random.shuffle(simbolos)
        self.cartas = [Carta(s) for s in simbolos]
        self.filas = filas
        self.columnas = columnas

    def obtener_carta(self, fila, col):
        return self.cartas[fila * self.columnas + col]


# ========================
# Clase Juego (con GUI)
# ========================
class JuegoMemorama:
    def __init__(self, root, jugador, filas=4, columnas=4, tiempo_inicial=60):
        self.root = root
        self.jugador = jugador
        self.tablero = Tablero(filas, columnas)
        self.intentos = 0
        self.selecciones = []
        self.tiempo = tiempo_inicial
        self.tiempo_restante = tiempo_inicial

        root.title(f"🧠 Memorama - Nivel {self.jugador.nivel}")
        root.geometry("500x500")

        # Reloj
        self.label_tiempo = tk.Label(root, text=f"⏳ Tiempo: {self.tiempo_restante}", font=("Arial", 14))
        self.label_tiempo.grid(row=0, column=0, columnspan=columnas)

        # Tablero de botones
        self.botones = []
        for f in range(self.tablero.filas):
            fila = []
            for c in range(self.tablero.columnas):
                boton = tk.Button(root, text="❓", width=8, height=4,
                                  command=lambda f=f, c=c: self.voltear_carta(f, c))
                boton.grid(row=f+1, column=c, padx=5, pady=5)
                fila.append(boton)
            self.botones.append(fila)

        # Iniciar temporizador
        self.actualizar_tiempo()

    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.config(text=f"⏳ Tiempo: {self.tiempo_restante}")
            self.root.after(1000, self.actualizar_tiempo)
        else:
            messagebox.showwarning("⏰ Tiempo agotado", "¡Se acabó el tiempo!")
            self.root.destroy()

    def voltear_carta(self, fila, col):
        carta = self.tablero.obtener_carta(fila, col)
        if carta.esta_emparejada() or carta in [self.tablero.obtener_carta(f, c) for f, c in self.selecciones]:
            return

        carta.voltear()
        self.botones[fila][col].config(text=carta.mostrar())
        self.selecciones.append((fila, col))

        if len(self.selecciones) == 2:
            self.root.after(1000, self.verificar_par)

    def verificar_par(self):
        (f1, c1), (f2, c2) = self.selecciones
        carta1 = self.tablero.obtener_carta(f1, c1)
        carta2 = self.tablero.obtener_carta(f2, c2)

        if carta1.es_igual(carta2):
            carta1.emparejar()
            carta2.emparejar()
            self.jugador.aumentar_puntaje()

            # Carta especial ⏰
            if carta1.get_simbolo() == "⏰":
                self.tiempo_restante += 10
                self.label_tiempo.config(text=f"⏳ Tiempo: {self.tiempo_restante}")
                messagebox.showinfo("🎁 Bonificación", "¡Ganaste +10 segundos!")

        else:
            carta1.voltear()
            carta2.voltear()

        # Actualizar botones
        for f in range(self.tablero.filas):
            for c in range(self.tablero.columnas):
                carta = self.tablero.obtener_carta(f, c)
                self.botones[f][c].config(text=carta.mostrar())

        self.selecciones = []
        self.intentos += 1

        # Verificar fin del juego
        if all(carta.esta_emparejada() for carta in self.tablero.cartas):
            messagebox.showinfo("🎉 ¡Ganaste!",
                                f"Jugador: {self.jugador.get_nombre()}\n"
                                f"Pares encontrados: {self.jugador.get_puntaje()}\n"
                                f"Intentos: {self.intentos}\n"
                                f"Nivel alcanzado: {self.jugador.nivel}")
            self.jugador.subir_nivel()
            self.root.destroy()
            self.siguiente_nivel()

    def siguiente_nivel(self):
        root = tk.Tk()
        # Aumenta dificultad: más columnas y menos tiempo
        JuegoMemorama(root, self.jugador, filas=4, columnas=4+self.jugador.nivel, tiempo_inicial=60 - (self.jugador.nivel*5))
        root.mainloop()


# ========================
# Programa Principal
# ========================
if __name__ == "__main__":
    nombre = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre)

    root = tk.Tk()
    juego = JuegoMemorama(root, jugador)
    root.mainloop()

