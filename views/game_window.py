import tkinter as tk
from PIL import Image, ImageTk

from levels.principiante import Principiante
from levels.amateur import Amateur
from levels.experto import Experto

class GameWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Smart Horses")
        self.geometry("600x430")
        self.config(bg="white")

        # Imagen de título
        img = Image.open("resources/images/Smart Horses.png")
        img = img.resize((610, 200))  # Resize the image
        self.photo = ImageTk.PhotoImage(img)
        self.tituloHorses = tk.Label(self, image=self.photo)
        self.tituloHorses.pack(pady=10)
        self.tituloHorses.config(bg="white")
        self.tituloHorses.place(x=0, y=0)

        # Imágenes de niveles
        # Carga la imagen nivel principiante
        imagePrincipiante = Image.open("resources/images/level_principiante.png")
        imagePrincipiante = imagePrincipiante.resize((100, 50))
        self.btnPrincipiante_img = ImageTk.PhotoImage(imagePrincipiante)

        # Carga la imagen nivel amateur
        imageAmateur = Image.open("resources/images/level_amateur.png")
        imageAmateur = imageAmateur.resize((100, 50))
        self.btnAmateur_img = ImageTk.PhotoImage(imageAmateur)

        # Carga la imagen nivel experto
        imageExperto = Image.open("resources/images/level_experto.png")
        imageExperto = imageExperto.resize((100, 50))
        self.btnExperto_img = ImageTk.PhotoImage(imageExperto)

        # Carga la imagen para reiniciar
        imageReiniciar = Image.open("resources/images/reiniciar.png")
        imageReiniciar = imageReiniciar.resize((100, 50))
        self.btnReinicio_img = ImageTk.PhotoImage(imageReiniciar)

        # Nivel de dificultad
        self.difficultLabel = tk.Label(self, text="Escoge la dificultad del juego ")
        self.difficultLabel.pack()
        self.difficultLabel.config(font=('Times New Roman', 15), bg="white", fg="black")
        self.difficultLabel.place(x=190, y=160)

        # Botones de dificultad
        self.botonPrincipiante = tk.Button(self, image=self.btnPrincipiante_img, bg="white", bd=0, command=self.level_one)
        self.botonPrincipiante.pack()
        self.botonPrincipiante.place(x=250, y=210)

        self.botonAmateur = tk.Button(self, image=self.btnAmateur_img, bg="white", bd=0, command=self.level_two)
        self.botonAmateur.pack()
        self.botonAmateur.place(x=250, y=280)

        self.botonExperto = tk.Button(self, image=self.btnExperto_img, bg="white", bd=0, command=self.level_three)
        self.botonExperto.pack()
        self.botonExperto.place(x=250, y=350)

    def level_one(self):
        Principiante()

    def level_two(self):
        Amateur()

    def level_three(self):
        Experto()