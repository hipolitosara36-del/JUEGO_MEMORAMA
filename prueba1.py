import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class Carta:
    def __init__(self, simbolo, imagen):
        self.__simbolo = simbolo
        self.__imagen = imagen
        self.__visible = False
        self.__emparejada = False

    def voltear(self):
        if not self.__emparejada:
            self.__visible = not self.__visible

    def mostrar(self):
        if self.__visible or self.__emparejada:
            return self.__imagen
        return None

    def es_igual(self, otra_carta):
        return self.__simbolo == otra_carta.__simbolo

    def emparejar(self):
        self.__emparejada = True

    def esta_emparejada(self):
        return self.__emparejada

    def get_simbolo(self):
        return self.__simbolo


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


class Tablero:
    def __init__(self, filas, columnas, carpeta="imagenes", tamaño=(100, 100), incluir_especial=True):
        archivos = os.listdir(carpeta)
        archivos = [f for f in archivos if f.endswith(".png") or f.endswith(".jpg")]

        if len(archivos) < (filas * columnas) // 2:
            raise ValueError("⚠️ No hay suficientes imágenes en la carpeta.")

        simbolos = random.sample(archivos, (filas * columnas) // 2)
        simbolos = simbolos * 2

        if incluir_especial and "clock.png" in archivos and len(simbolos) >= 2:
            simbolos[-2:] = ["clock.png", "clock.png"]

        random.shuffle(simbolos)

        self.cartas = []
        self.imagenes = []

        for archivo in simbolos:
            ruta = os.path.join(carpeta, archivo)
            img = Image.open(ruta).resize(tamaño, Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            self.imagenes.append(foto)
            self.cartas.append(Carta(archivo, foto))

        self.filas = filas
        self.columnas = columnas

    def obtener_carta(self, fila, col):
        return self.cartas[fila * self.columnas + col]


class JuegoMemorama:
    def __init__(self, root, jugador, filas, columnas, tiempo_inicial=30):
        self.root = root
        self.jugador = jugador
        self.tablero = Tablero(filas, columnas)
        self.intentos = 0
        self.selecciones = []
        self.tiempo_restante = tiempo_inicial
        self.timer_id = None

        root.title(f"🧠 Memorama con Imágenes - Nivel {self.jugador.nivel}")

        self.label_tiempo = tk.Label(root, text=f"⏳ Tiempo: {self.tiempo_restante}", font=("Arial", 14))
        self.label_tiempo.grid(row=0, column=0, columnspan=columnas)

        self.botones = []
        for f in range(self.tablero.filas):
            fila = []
            for c in range(self.tablero.columnas):
                boton = tk.Button(root, text="❓", command=lambda f=f, c=c: self.voltear_carta(f, c))
                boton.grid(row=f+1, column=c, padx=5, pady=5, sticky="nsew")
                fila.append(boton)
            self.botones.append(fila)

        for c in range(columnas):
            root.grid_columnconfigure(c, weight=1)
        for f in range(filas):
            root.grid_rowconfigure(f+1, weight=1)

        self.actualizar_tiempo()

    def actualizar_tiempo(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            self.label_tiempo.config(text=f"⏳ Tiempo: {self.tiempo_restante}")
            self.timer_id = self.root.after(1000, self.actualizar_tiempo)
        else:
            messagebox.showwarning("⏰ Tiempo agotado", "¡Se acabó el tiempo!")
            self.root.destroy()

    def voltear_carta(self, fila, col):
        carta = self.tablero.obtener_carta(fila, col)
        if carta.esta_emparejada() or carta in [self.tablero.obtener_carta(f, c) for f, c in self.selecciones]:
            return

        carta.voltear()
        if carta.mostrar():
            self.botones[fila][col].config(image=carta.mostrar(), text="")
        else:
            self.botones[fila][col].config(text="❓", image="")

        self.selecciones.append((fila, col))
        if len(self.selecciones) == 2:
            self.root.after(800, self.verificar_par)

    def verificar_par(self):
        (f1, c1), (f2, c2) = self.selecciones
        carta1 = self.tablero.obtener_carta(f1, c1)
        carta2 = self.tablero.obtener_carta(f2, c2)

        if carta1.es_igual(carta2):
            carta1.emparejar()
            carta2.emparejar()
            self.jugador.aumentar_puntaje()

            if carta1.get_simbolo() == "clock.png":
                self.tiempo_restante += 10
                self.label_tiempo.config(text=f"⏳ Tiempo: {self.tiempo_restante}")
                messagebox.showinfo("🎁 Bonificación", "¡Ganaste +10 segundos!")

        else:
            carta1.voltear()
            carta2.voltear()
            self.botones[f1][c1].config(text="❓", image="")
            self.botones[f2][c2].config(text="❓", image="")

        self.selecciones = []
        self.intentos += 1

        if all(carta.esta_emparejada() for carta in self.tablero.cartas):
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

            messagebox.showinfo("🎉 ¡Ganaste!",
                                f"Jugador: {self.jugador.get_nombre()}\n"
                                f"Pares: {self.jugador.get_puntaje()}\n"
                                f"Intentos: {self.intentos}\n"
                                f"Nivel: {self.jugador.nivel}")

            self.jugador.subir_nivel()
            self.root.destroy()
            self.siguiente_nivel()

    def siguiente_nivel(self):
        filas = 2 + (self.jugador.nivel - 1)
        columnas = 2 + (self.jugador.nivel - 1)
        total_cartas = filas * columnas
        necesarias = total_cartas // 2

        carpeta = "imagenes"
        archivos = os.listdir(carpeta)
        imagenes_validas = [f for f in archivos if f.endswith(".png") or f.endswith(".jpg")]
        max_pares = len(imagenes_validas)

        if necesarias > max_pares:
            ventana = tk.Tk()
            ventana.title("🚫 Fin del juego")

            mensaje = tk.Label(ventana, text=f"No hay suficientes imágenes para el nivel {self.jugador.nivel}.\n"
                                             f"Imágenes disponibles: {max_pares}\n"
                                             f"Pares requeridos: {necesarias}\n\n"
                                             f"¿Quieres reiniciar el juego, {self.jugador.get_nombre()}?",
                               font=("Arial", 12), padx=20, pady=20)
            mensaje.pack()

            def reiniciar():
                ventana.destroy()
                self.jugador.nivel = 1
                self.jugador._Jugador__puntaje = 0
                root = tk.Tk()
                JuegoMemorama(root, self.jugador, filas=2, columnas=2, tiempo_inicial=30)
                root.mainloop()

            boton_reiniciar = tk.Button(ventana, text="🔄 Reiniciar juego", command=reiniciar, font=("Arial", 12))
            boton_reiniciar.pack(pady=10)

            ventana.mainloop()
            return

        tiempo = max(20, 40 - (self.jugador.nivel * 2))

        root = tk.Tk()
        JuegoMemorama(root, self.jugador, filas, columnas, tiempo_inicial=tiempo)
        root.mainloop()


if __name__ == "__main__":
    nombre = input("Ingresa tu nombre:")
    jugador = Jugador(nombre)
    root = tk.Tk()
    juego = JuegoMemorama(root, jugador, filas=2, columnas=2, tiempo_inicial=30)
    root.mainloop()