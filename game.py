import numpy as np
from node import Nodo
import copy
import random

class Juego:
    def __init__(self):
        self.tableroGame = np.zeros((8, 8), dtype=int)
        self.jugadorGame = 'Max'
        self.puntajeMin = 0
        self.puntajeMax = 0
        self.tiene_x2_max = False
        self.tiene_x2_min = False
        self.posicionJugadorMax = []
        self.posicionJugadorMin = []
        self.max_last_move = None

        self.horse_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def complejidad_juego(self, nivelFront):
        if nivelFront == 'principiante':
            profundidadGame = 2
        elif nivelFront == 'amateur':
            profundidadGame = 4
        elif nivelFront == 'experto':
            profundidadGame = 6
        return profundidadGame

    def generar_tablero(self, reset=False):
        if reset or np.count_nonzero(self.tableroGame) == 0:
            self.tableroGame = np.zeros((8, 8), dtype=int)
            
            numeros = list(range(1, 11)) 
            for num in numeros:
                while True:
                    posicion = np.random.randint(8*8)
                    fila, columna = np.unravel_index(posicion, (8, 8))
                    if self.tableroGame[fila, columna] == 0:
                        self.tableroGame[fila, columna] = num
                        break

            # Asignar las casillas con x2
            for _ in range(4):  # Hay cuatro casillas x2
                while True:
                    posicion = np.random.randint(8 * 8)
                    fila, columna = np.unravel_index(posicion, (8, 8))
                    if self.tableroGame[fila, columna] == 0:
                        self.tableroGame[fila, columna] = 20  # Representar x2 con 20
                        break

            while True:
                # Posición del jugador Max
                posicion = np.random.randint(8*8)
                fila, columna = np.unravel_index(posicion, (8, 8))
                if self.tableroGame[fila, columna] == 0:
                    self.tableroGame[fila, columna] = 11 
                    self.posicionJugadorMax = (columna, fila)
                    break

            while True:
                # Posición del jugador Min
                posicion = np.random.randint(8*8)
                fila, columna = np.unravel_index(posicion, (8, 8))
                if self.tableroGame[fila, columna] == 0:
                    self.tableroGame[fila, columna] = 12
                    self.posicionJugadorMin = (columna, fila)
                    break

        return self.tableroGame, self.posicionJugadorMax, self.posicionJugadorMin

    def obtener_tablero(self, reset=False):
        if reset or np.count_nonzero(self.tableroGame) == 0:
            self.tableroGame, self.posicionJugadorMax, self.posicionJugadorMin = self.generar_tablero(reset=True)
        return self.tableroGame, self.posicionJugadorMax, self.posicionJugadorMin

    def juego_terminado(self, tablero):
        numeros = list(range(1, 11)) 
        terminado = False
        for fila in tablero:
            for numero in fila:
                if numero in numeros:
                    return False
        return True

    def casilla_puntos(self, tablero, fila, columna):
        if tablero[fila][columna] in range(1, 11): 
            return True
        else:
            return False
        
    def movimientos_posibles(self, tablero, jugador):
        jugadas_posibles = []
        posiciones_visitadas = set()

        def buscar_movimiento(fila, columna, fila_anterior, columna_anterior):
            if fila < 0 or fila >= 8 or columna < 0 or columna >= 8 or (fila, columna) in posiciones_visitadas:
                return
            posiciones_visitadas.add((fila, columna))
            if self.alcanzar_casilla(tablero, jugador, fila, columna):
                jugada = (fila, columna)
                jugadas_posibles.append(jugada)
            else:
                # Evitar volver a la posición anterior inmediatamente
                if fila != fila_anterior or columna != columna_anterior:
                    buscar_movimiento(fila - 1, columna, fila, columna)  # Movimiento hacia arriba
                    buscar_movimiento(fila + 1, columna, fila, columna)  # Movimiento hacia abajo
                    buscar_movimiento(fila, columna - 1, fila, columna)  # Movimiento hacia la izquierda
                    buscar_movimiento(fila, columna + 1, fila, columna)  # Movimiento hacia la derecha

        posicionActual = self.obtener_posicion_caballo(tablero, jugador)
        if posicionActual is not None:
            buscar_movimiento(posicionActual[0], posicionActual[1], -1, -1)  # -1, -1 para evitar la posición anterior

        return jugadas_posibles

    def alcanzar_casilla(self, tablero, jugador, fila, columna):
        posicionActual = self.obtener_posicion_caballo(tablero, jugador)
        if posicionActual is None:
            return False
        if tablero[fila][columna] not in [11, 12]:
            distanciaFila = abs(fila - posicionActual[0])
            distanciaColumna = abs(columna - posicionActual[1])
            if (distanciaFila == 2 and distanciaColumna == 1) or (distanciaFila == 1 and distanciaColumna == 2):
                return True
            else:
                return False

    def obtener_posicion_caballo(self, tablero, jugador):
        for i in range(len(tablero)):
            for j in range(len(tablero)):
                if jugador == 'Max' and tablero[i][j] == 11:
                    self.max_last_move = (i, j)
                    return (i, j)
                if jugador == 'Min' and tablero[i][j] == 12:
                    return (i, j)
        return None

    # arreglar puntaje para que se muestre el verdadero
    def realizarJugada(self, tablero, jugada, jugador):
        fila, columna = jugada[0], jugada[1]
        new = tablero.copy()

        # Borrar la posición anterior del jugador en el nuevo tablero
        jugador_actual = 11 if jugador == 'Max' else 12
        posicion_anterior = np.where(new == jugador_actual)
        new[posicion_anterior] = 0

        if tablero[fila, columna] == 20:  # Si recoge un x2
            if jugador == 'Max':
                self.tiene_x2_max = True
            else:
                self.tiene_x2_min = True
        elif self.casilla_puntos(tablero, fila, columna):
            puntaje = tablero[fila, columna]
            if (jugador == 'Max' and self.tiene_x2_max) or (jugador == 'Min' and self.tiene_x2_min):
                puntaje *= 2
                if jugador == 'Max':
                    self.tiene_x2_max = False
                else:
                    self.tiene_x2_min = False
            self.sumar_puntaje(jugador, puntaje)
        else:
            if jugador == 'Max':
                self.tiene_x2_max = False
            else:
                self.tiene_x2_min = False
        if jugador == 'Max':
            new[fila, columna] = 11
        elif jugador == 'Min':
            new[fila, columna] = 12
        return new

    def sumar_puntaje(self, jugador, puntuacion):
        if jugador == 'Max':
            self.puntajeMax += puntuacion
        elif jugador == 'Min':
            self.puntajeMin += puntuacion

    def obtener_puntaje(self, jugador):
        if jugador == 'Max':
            return self.puntajeMax
        elif jugador == 'Min':
            return self.puntajeMin

    def oponente(self, jugador):
        if jugador == 'Max':
            return 'Min'
        else:
            return 'Max'

    def evaluar_estado(self, profundidad):
        # Evaluación base de la diferencia de puntuación
        diferencia_puntuacion = self.puntajeMax - self.puntajeMin
        
        # Evaluar posición actual
        posicion_actual = self.obtener_posicion_caballo(self.tableroGame, 'Max')
        if posicion_actual is None:
            return diferencia_puntuacion
        
        x, y = posicion_actual
        valor_casilla_actual = self.tableroGame[x][y]

        # Verificar si la posición actual tiene puntos
        if self.casilla_puntos(self.tableroGame, x, y):
            # Multiplicador x2 si está disponible
            multiplicador = 2 if self.tiene_x2_max else 1
            # Dar un peso muy alto a casillas con puntos
            return 1000 * multiplicador * valor_casilla_actual + diferencia_puntuacion
        elif valor_casilla_actual == 20:  # Casilla x2
            return 50 + diferencia_puntuacion
        else:
            return (diferencia_puntuacion)

    def minimax(self, nodo, alfa, beta, movimientos_realizados):
        if nodo.profundidad == 0 or self.juego_terminado(nodo.tablero):
            return self.evaluar_estado(nodo.profundidad)

        if nodo.jugador == 'Min':
            movimientos = self.movimientos_posibles(nodo.tablero, nodo.jugador)

            # Solo filtrar el último movimiento para evitar ciclos
            if self.max_last_move is not None:
                movimientos = [m for m in movimientos if m != self.max_last_move]
                if not movimientos:
                    movimientos = self.movimientos_posibles(nodo.tablero, nodo.jugador)

            mejorValor = -float("inf")
            for jugada in movimientos:
                if jugada not in movimientos_realizados:
                    movimientos_realizados.append(jugada)
                    nuevoTablero = self.realizarJugada(copy.deepcopy(nodo.tablero), jugada, nodo.jugador)
                    nuevoNodo = Nodo(nuevoTablero, self.oponente(nodo.jugador), nodo.profundidad - 1)
                    valor = self.minimax(nuevoNodo, alfa, beta, movimientos_realizados)
                    mejorValor = max(mejorValor, valor)
                    alfa = max(alfa, mejorValor)
                    movimientos_realizados.remove(jugada)
                    if beta <= alfa:
                        break
            return mejorValor
        else:  # Jugador Min
            movimientos = self.movimientos_posibles(nodo.tablero, nodo.jugador)
            mejorValor = float("inf")
            
            for jugada in movimientos:
                if jugada not in movimientos_realizados:
                    movimientos_realizados.append(jugada)
                    nuevoTablero = self.realizarJugada(copy.deepcopy(nodo.tablero), jugada, nodo.jugador)
                    nuevoNodo = Nodo(nuevoTablero, self.oponente(nodo.jugador), nodo.profundidad - 1)
                    valor = self.minimax(nuevoNodo, alfa, beta, movimientos_realizados)
                    mejorValor = min(mejorValor, valor)
                    beta = min(beta, mejorValor)
                    movimientos_realizados.remove(jugada)
                    if beta <= alfa:
                        break
            return mejorValor

def verificar_primer_movimiento_max(tablero, profundidad, jugador, movimientos_realizados):
    juego = Juego()
    movimientos_iniciales = juego.movimientos_posibles(tablero, jugador)
    mejor_utilidad = -float('inf')
    alfa = -float("inf")
    beta = float("inf")
    mejor_movimiento = None

    for movimiento in movimientos_iniciales:
        if movimiento not in movimientos_realizados:
            movimientos_realizados.append(movimiento)
            nuevo_tablero = juego.realizarJugada(copy.deepcopy(tablero), movimiento, jugador)
            nuevo_nodo = Nodo(nuevo_tablero, juego.oponente(jugador), profundidad - 1)
            utilidad = juego.minimax(nuevo_nodo, alfa, beta, movimientos_realizados)
            if utilidad > mejor_utilidad:
                mejor_utilidad = utilidad
                mejor_movimiento = movimiento
            movimientos_realizados.remove(movimiento)

    if mejor_movimiento is None:
        print("No se encontró un mejor movimiento")
        mejor_movimiento = random.choice(movimientos_iniciales)

    return mejor_movimiento
