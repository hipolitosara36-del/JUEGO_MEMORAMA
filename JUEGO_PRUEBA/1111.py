import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class Tablero:
    def __init__(self, filas, columnas, imagenes):
        self.filas = filas
        self.columnas = columnas
        total_cartas = filas * columnas

        imagenes = imagenes[:total_cartas // 2]
        cartas = imagenes * 2
        random.shuffle(cartas)

        self.cartas = cartas

    def obtener_carta(self, fila, col):
        return self.cartas[fila * self.columnas + col]

class JuegoMemorama:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Memorama")
        self.imagenes = self.cargar_imagenes()
        self.imagen_placeholder = self.cargar_placeholder()

        self.nivel = 1
        self.cartas_volteadas = []
        self.botones = {}
        self.pares_encontrados = 0
        self.tiempo = 30
        self.temporizador_activo = False

        self.iniciar_juego()

    def cargar_imagenes(self, size=(80, 80)):
        ruta = "imagenes"
        imagenes = []
        for archivo in os.listdir(ruta):
            if archivo.endswith(".png") or archivo.endswith(".jpg"):
                img = Image.open(os.path.join(ruta, archivo))
                img = img.resize(size, Image.LANCZOS)
                imagenes.append(ImageTk.PhotoImage(img))
        return imagenes

    def cargar_placeholder(self, size=(80, 80)):
        ruta = "imagenes/interrogacion.png"
        if os.path.exists(ruta):
            img = Image.open(ruta).resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        else:
            # Fallback si no hay imagen de interrogación
            img = Image.new("RGB", size, color="gray")
            return ImageTk.PhotoImage(img)

    def iniciar_juego(self):
        filas = columnas = 2 * self.nivel
        self.tablero = Tablero(filas, columnas, self.imagenes)

        self.cartas_volteadas = []
        self.pares_encontrados = 0
        self.tiempo = 30 + (self.nivel - 1) * 15
        self.temporizador_activo = True

        self.dibujar_tablero(filas, columnas)
        self.actualizar_tiempo()

    def dibujar_tablero(self, filas, columnas):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.botones = {}
        for f in range(filas):
            for c in range(columnas):
                boton = tk.Button(self.root, image=self.imagen_placeholder,
                                  borderwidth=0, highlightthickness=0,
                                  command=lambda f=f, c=c: self.voltear_carta(f, c))
                boton.grid(row=f, column=c, padx=5, pady=5)
                self.botones[(f, c)] = boton

        self.label_tiempo = tk.Label(self.root, text=f"Tiempo: {self.tiempo}", font=("Arial", 12))
        self.label_tiempo.grid(row=filas, column=0, columnspan=columnas, pady=10)

    def voltear_carta(self, fila, col):
        if len(self.cartas_volteadas) == 2:
            return

        boton = self.botones[(fila, col)]
        carta = self.tablero.obtener_carta(fila, col)

        boton.config(image=carta, state="disabled")
        boton.image = carta  # mantener referencia
        self.cartas_volteadas.append((fila, col, carta))

        if len(self.cartas_volteadas) == 2:
            self.root.after(1000, self.verificar_pareja)

    def verificar_pareja(self):
        (f1, c1, carta1), (f2, c2, carta2) = self.cartas_volteadas
        if carta1 == carta2:
            self.pares_encontrados += 1
        else:
            self.botones[(f1, c1)].config(image=self.imagen_placeholder, state="normal")
            self.botones[(f2, c2)].config(image=self.imagen_placeholder, state="normal")

        self.cartas_volteadas = []

        if self.pares_encontrados == len(self.tablero.cartas) // 2:
            self.temporizador_activo = False
            messagebox.showinfo("¡Ganaste!", f"Nivel {self.nivel} completado 🎉")
            self.nivel += 1
            self.iniciar_juego()

    def actualizar_tiempo(self):
        if self.temporizador_activo:
            if self.tiempo > 0:
                self.tiempo -= 1
                self.label_tiempo.config(text=f"Tiempo: {self.tiempo}")
                self.root.after(1000, self.actualizar_tiempo)
            else:
                messagebox.showinfo("Fin del juego", "Se acabó el tiempo ⏳")
                self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoMemorama(root)
    root.mainloop()