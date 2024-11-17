class Nodo:
    def __init__(self, tablero, jugador, profundidad):
        self.tablero = tablero
        self.jugador = jugador
        self.profundidad = profundidad

    def obtener_utilidad(self):
        # Implementa aquí la lógica para obtener la utilidad del nodo

        utilidad = 0
        # Aquí puedes calcular la utilidad del nodo en función de su tablero y jugador actual
        # Puedes acceder a la matriz del tablero con self.tablero y al jugador con self.jugador

        # Ejemplo: calcular la suma de los valores en el tablero para el jugador Max
        if self.jugador == 'Max':
            utilidad = sum(sum(self.tablero))

        return utilidad