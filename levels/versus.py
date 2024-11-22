import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image, ImageTk
from smart_horses_game import SmartHorsesGame  # Importar la clase del juego

class SmartHorsesGUI(tk.Toplevel):
    def __init__(self, depth_horse1, depth_horse2):
        super().__init__()
        
        # Configurar juego
        self.game = SmartHorsesGame()
        self.depth_horse1 = depth_horse1
        self.depth_horse2 = depth_horse2
        self.current_horse = 1
        
        # Configuración de ventana
        self.title("Smart Horses Game")
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        # Etiquetas de puntuación
        self.score_horse1_label = tk.Label(self, text="Puntuación Caballo Blanco: 0")
        self.score_horse1_label.pack()

        self.score_horse2_label = tk.Label(self, text="Puntuación Caballo Negro: 0")
        self.score_horse2_label.pack()

        # Botón de siguiente paso
        self.next_button = tk.Button(self, text="Siguiente paso", command=self.make_move)
        self.next_button.pack()

        # Inicializar visualización
        self.update_board()

    def update_board(self):
        """Actualizar representación visual del tablero"""
        self.canvas.delete("all")

        for fila in range(8):
            for columna in range(8):
                x = columna * 50
                y = fila * 50

                # Colores de las casillas
                color = "beige" if (fila + columna) % 2 == 0 else "gray"
                self.canvas.create_rectangle(x, y, x + 50, y + 50, fill=color)

                # Dibujar puntos
                if self.game.points_board[fila, columna] > 0:
                    self.canvas.create_text(
                        x + 25, y + 25, 
                        text=str(self.game.points_board[fila, columna]), 
                        font=("Arial", 12)
                    )

                # Dibujar símbolos x2
                if self.game.x2_board[fila, columna]:
                    self.canvas.create_text(
                        x + 25, y + 25, 
                        text="x2", 
                        font=("Arial", 12, "bold"), 
                        fill="red"
                    )

        # Dibujar caballos
        horse1_x, horse1_y = self.game.horse1_pos
        horse2_x, horse2_y = self.game.horse2_pos

        # Cargar imágenes de caballos
        self.img_horse1 = self.load_horse_image("blanco")
        self.img_horse2 = self.load_horse_image("negro")

        self.canvas.create_image(
            horse1_y * 50 + 25, horse1_x * 50 + 25, 
            image=self.img_horse1, tags="horse1"
        )
        self.canvas.create_image(
            horse2_y * 50 + 25, horse2_x * 50 + 25, 
            image=self.img_horse2, tags="horse2"
        )

        # Actualizar etiquetas de puntuación
        self.score_horse1_label.config(text=f"Puntuación Caballo Blanco: {self.game.horse1_score}")
        self.score_horse2_label.config(text=f"Puntuación Caballo Negro: {self.game.horse2_score}")

    def load_horse_image(self, color: str):
        """Cargar imagen de caballo"""
        try:
            img = Image.open(f"resources/images/caballo_{color}.png")
            img = img.resize((40, 40), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Imagen de caballo {color} no encontrada. Usando texto.")
            return None

    def make_move(self):
        """Realizar movimiento del caballo actual"""
        if self.game.game_over():
            self.declare_winner()
            return
        
        if self.current_horse == 1:
            best_move, _ = self.game.minimax_horse1(self.depth_horse1, True)
            if best_move:
                self.game.mover(1, best_move)
        else:
            best_move, _ = self.game.minimax_horse2(self.depth_horse2, True)
            if best_move:
                self.game.mover(2, best_move)
        
        if best_move is None:
            print(f"No hay movimientos posibles para Caballo {self.current_horse}")
            self.current_horse = 3 - self.current_horse  # Cambiar de caballo
            return
        
        # Actualizar visualización
        self.update_board()

        # Cambiar de caballo
        self.current_horse = 3 - self.current_horse

        # Verificar si el juego ha terminado
        if self.game.game_over():
            self.declare_winner()

    def declare_winner(self):
        """Declarar el ganador del juego"""
        if self.game.horse1_score > self.game.horse2_score:
            winner = "Caballo 1"
        elif self.game.horse2_score > self.game.horse1_score:
            winner = "Caballo 2"
        else:
            winner = "Empate"

        messagebox.showinfo("Juego terminado", f"¡Ganador: {winner}!")
        self.destroy()