import tkinter as tk
from tkinter import ttk
from levels.versus import SmartHorsesGUI  

class JuegoInterface:
    def __init__(self):
        self.raiz = tk.Tk()
        self.raiz.title("Competencia entre Minimax y Minimax2")
        
        # Variables de dificultad
        self.dificultad_minimax1 = tk.StringVar()
        self.dificultad_minimax2 = tk.StringVar()
        
        # Variables para los Combobox
        self.combo_minimax1 = None
        self.combo_minimax2 = None
        
        # Configuración de la ventana
        self.setup_interface()
        
        self.raiz.mainloop()
     
    def setup_interface(self):
        # Etiquetas
        tk.Label(self.raiz, text="Nivel de dificultad para Minimax1").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.raiz, text="Nivel de dificultad para Minimax2").grid(row=1, column=0, padx=10, pady=10)
        
        # Menús desplegables
        opciones = ["principiante", "amateur", "experto"]
        
        self.combo_minimax1 = ttk.Combobox(self.raiz, values=opciones, state="readonly")
        self.combo_minimax1.grid(row=0, column=1, padx=10, pady=10)
        
        self.combo_minimax2 = ttk.Combobox(self.raiz, values=opciones, state="readonly")
        self.combo_minimax2.grid(row=1, column=1, padx=10, pady=10)
        
        # Botón para iniciar la competencia
        tk.Button(self.raiz, text="Iniciar Competencia", command=self.iniciar_competencia).grid(row=2, column=0, columnspan=2, pady=20)
    
    def iniciar_competencia(self):
        # Mapear dificultades a profundidades de árbol
        dificultades = {
            "principiante": 2,
            "amateur": 4,
            "experto": 6
        }
        
        # Verificar que se hayan seleccionado ambas dificultades
        dificultad1 = self.combo_minimax1.get()
        dificultad2 = self.combo_minimax2.get()
        
        if not dificultad1 or not dificultad2:
            tk.messagebox.showerror("Error", "Se debe elegir un nivel de dificultad para ambos jugadores")
            return
        
        # Convertir dificultades a profundidades
        depth_horse1 = dificultades.get(dificultad1)
        depth_horse2 = dificultades.get(dificultad2)
        
        # Crear ventana de juego con las profundidades correspondientes
        self.raiz.destroy()
        game_gui = SmartHorsesGUI(depth_horse1=depth_horse1, depth_horse2=depth_horse2)