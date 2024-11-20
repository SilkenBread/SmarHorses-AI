import tkinter as tk
from PIL import Image, ImageTk
from views.game_window import GameWindow


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Horses")
        self.geometry("600x600")
        self.config(bg="white")

        # Imagen de titulo
        img = Image.open("resources/images/Smart Horses.png")
        img = img.resize((610, 200))  # Resize the image
        self.photo = ImageTk.PhotoImage(img)
        self.tituloHorses = tk.Label(self, image=self.photo)
        self.tituloHorses.pack(pady=10)
        self.tituloHorses.config(bg="white")
        self.tituloHorses.place(x=0, y=0)

        # Carga la imagen jugar
        imageJugar = Image.open("resources/images/jugar.png")
        imageJugar = imageJugar.resize((200, 100))  # Ajusta el tamaño de la imagen si es necesario
        self.btnJugar_img = ImageTk.PhotoImage(imageJugar)

        def game():
            GameWindow()
        
        # Crea el botón con la imagen jugar y creditos
        self.botonJugar = tk.Button(self, image=self.btnJugar_img, bg="white", bd=0, command=game)
        self.botonJugar.pack()
        self.botonJugar.place(x= 200, y= 200)
