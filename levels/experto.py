import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from game import Juego
from game import verificar_primer_movimiento_max


class Experto(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.juego = Juego()
        self.profundidad = self.juego.complejidad_juego('experto')
        self.jugador = 'Max'
        self.movimientos_realizados = set()  # Registro de movimientos realizados

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        self.score_min_label = tk.Label(self, text="Puntuación Min: ")
        self.score_min_label.pack()

        self.score_max_label = tk.Label(self, text="Puntuación Max: ")
        self.score_max_label.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.update_board()

        self.after(1000, self.make_initial_move) # Esperar 2 segundos antes del primer movimiento


    def update_scores(self):
        self.score_min_label.config(
            text="Puntuación Min: " + str(self.juego.puntajeMin))
        self.score_max_label.config(
            text="Puntuación Max: " + str(self.juego.puntajeMax))


    def update_board(self):
        tablero, _, _ = self.juego.obtener_tablero(reset=False)

        self.canvas.delete("all")

        for fila in range(8):
            for columna in range(8):
                x = columna * 50
                y = fila * 50

                # Colores de las casillas
                color = "beige" if (fila + columna) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x, y, x + 50, y + 50, fill=color)

                if tablero[fila][columna] != 0:
                    if tablero[fila][columna] == 11:
                        self.img_caballoB = Image.open(
                            "resources/images/caballo_blanco.png")
                        self.img_caballoB = self.img_caballoB.resize(
                            (40, 40), Image.LANCZOS)
                        self.canvas.image_caballoB = ImageTk.PhotoImage(
                            self.img_caballoB)
                        self.canvas.create_image(
                            x + 25, y + 25, image=self.canvas.image_caballoB, tags="caballo_blanco")
                    elif tablero[fila][columna] == 12:
                        self.img_caballoN = Image.open(
                            "resources/images/caballo_negro.png")
                        self.img_caballoN = self.img_caballoN.resize(
                            (40, 40), Image.LANCZOS)
                        self.canvas.image_caballoN = ImageTk.PhotoImage(
                            self.img_caballoN)
                        self.canvas.create_image(
                            x + 25, y + 25, image=self.canvas.image_caballoN, tags="caballo_negro")
                    else:
                        # Números normales
                        self.canvas.create_text(
                            x + 25, y + 25, text=str(tablero[fila][columna]), font=("Arial", 12))


    def on_click(self, event):
        if self.jugador == 'Min':
            columna = event.x // 50
            fila = event.y // 50
            jugada_min = (fila, columna)

            if self.juego.alcanzar_casilla(self.juego.tableroGame, self.jugador, fila, columna):
                nuevo_tablero = self.juego.realizarJugada(
                    self.juego.tableroGame, jugada_min, self.jugador)
                self.update_board()

                if self.juego.juego_terminado(nuevo_tablero):
                    if self.juego.puntajeMin == self.juego.puntajeMax:
                        messagebox.showinfo(
                            "Juego terminado", "¡Es un empate!")
                        
                    elif self.juego.puntajeMin > self.juego.puntajeMax:
                        messagebox.showinfo("Juego terminado",
                                            "¡Le ganaste a la IA!")
                        
                    elif self.juego.puntajeMin < self.juego.puntajeMax:
                        messagebox.showinfo("Juego terminado",
                                            "¡Ganó la IA!")

                self.juego.tableroGame = nuevo_tablero

                self.jugador = 'Max'
                self.movimientos_realizados.add(jugada_min)
                self.make_move()

        elif self.jugador == 'Max':
            columna = event.x // 50
            fila = event.y // 50
            jugada_max = (fila, columna)

            if self.juego.alcanzar_casilla(self.juego.tableroGame, self.jugador, fila, columna):
                nuevo_tablero = self.juego.realizarJugada(
                    self.juego.tableroGame, jugada_max, self.jugador)
                self.update_board()

                if self.juego.juego_terminado(nuevo_tablero):
                    if self.juego.puntajeMax > self.juego.puntajeMin:
                        messagebox.showinfo("Juego terminado",
                                            "¡Ganó la IA!")
                        
                    elif self.juego.puntajeMin > self.juego.puntajeMax:
                        messagebox.showinfo("Juego terminado",
                                            "¡Le ganaste a la IA!")                 

                    elif self.juego.puntajeMin == self.juego.puntajeMax:
                        messagebox.showinfo(
                            "Juego terminado", "¡Es un empate!")
                        
                self.juego.tableroGame = nuevo_tablero

                self.jugador = 'Min'
                self.movimientos_realizados.add(jugada_max)
                self.make_move()

    
    def make_initial_move(self):
        self.make_move()

    
    # Función que muestra las posibles jugadas dibujadas en el tablero de juego
    def mostrar_posibles_jugadas(self, posibles_jugadas):
        for i, j in posibles_jugadas:
            x = j * 50 + 25
            y = i * 50 + 25
            self.canvas.create_oval(
                x - 20, y - 20, x + 20, y + 20, outline="green", width=2)
            
    def make_move(self):
        if self.jugador == 'Max':
            movimientos_realizados = self.movimientos_realizados.copy()  # Copia de los movimientos realizados
            mejor_movimiento_max = verificar_primer_movimiento_max(
                self.juego.tableroGame, self.profundidad, 'Max', movimientos_realizados)
            nuevo_tablero = self.juego.realizarJugada(
                self.juego.tableroGame, mejor_movimiento_max, 'Max')

            if self.juego.juego_terminado(nuevo_tablero):
                if self.juego.puntajeMax > self.juego.puntajeMin:
                    messagebox.showinfo("Juego terminado",
                                        "¡Ganó la IA!")
            self.juego.tableroGame = nuevo_tablero

            self.jugador = 'Min'

            self.update_scores()  # Actualizar puntuaciones en la interfaz

            self.update_board()

            self.mostrar_posibles_jugadas(self.juego.movimientos_posibles(
                nuevo_tablero, 'Min'))  # Mostrar posibles jugadas

        elif self.jugador == 'Min':
            movimientos_posibles_min = self.juego.movimientos_posibles(
                self.juego.tableroGame, 'Min')
            movimientos_posibles_min = movimientos_posibles_min - self.movimientos_realizados
            if not movimientos_posibles_min:
                if self.juego.puntajeMin == self.juego.puntajeMax:
                    messagebox.showinfo("Juego terminado", "¡Es un empate!")
                else:
                    messagebox.showinfo("Juego terminado",
                                        "¡Ganó el jugador 'Max'!")
                    
            else:
                self.make_move()