import numpy as np
from node import Nodo
import copy

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
        
    def utilidad_profundidad(self, profundidad):
        puntaje_max = self.obtener_puntaje('Max')
        puntaje_min = self.obtener_puntaje('Min')
        utilidad_puntaje = puntaje_max - puntaje_min
        if profundidad == 0:
            return utilidad_puntaje *0
        elif profundidad == 1:
            return utilidad_puntaje *6
        elif profundidad == 2:
            return utilidad_puntaje *5
        elif profundidad == 3:
            return utilidad_puntaje *4
        elif profundidad == 4:
            return utilidad_puntaje *3
        elif profundidad == 5:
            return utilidad_puntaje *2        
        elif profundidad == 6:
            return utilidad_puntaje *1
        else:
            return utilidad_puntaje

    def evaluar_estado(self, profundidad):
        puntaje_max = self.obtener_puntaje('Max')
        puntaje_min = self.obtener_puntaje('Min')
        puntos_disponibles = 0
        distancia_total = 0
        puede_tomar_punto = False  # Variable para verificar si 'Max' puede tomar un punto

        for fila in range(8):
            for columna in range(8):
                if self.casilla_puntos(self.tableroGame, fila, columna):
                    puntos_disponibles += 1
                    distancia = abs(fila - self.posicionJugadorMax[1]) + abs(columna - self.posicionJugadorMax[0])
                    distancia_total += distancia
                    puede_tomar_punto = True  # Se encontró al menos un punto disponible

        if puede_tomar_punto:
            return float('inf')  # 'Max' puede tomar un punto, se devuelve infinito

        if puntaje_max == 0 and puntaje_min == 0:
            return 0  # Ambos jugadores tienen puntaje 0, se considera empate

        if puntaje_max == puntos_disponibles:
            return float('inf')  # 'Max' ha recolectado todos los puntos

        utilidadProfundidad = self.utilidad_profundidad(profundidad)

        if distancia_total > 0:
            utilidadDistancia = puntos_disponibles / distancia_total
        else:
            utilidadDistancia = puntos_disponibles

        if puntos_disponibles > 0 and (puntaje_max == 0 or puntaje_max != 28):
            return -float('inf')  # No hay puntos y 'Max' no ha recolectado ninguno

        return puntaje_max - puntaje_min + utilidadProfundidad + utilidadDistancia


    def minimax(self, nodo, alfa, beta, movimientos_realizados):
        if nodo.profundidad == 0 or self.juego_terminado(nodo.tablero):
            return self.evaluar_estado(nodo.profundidad)

        if nodo.jugador == 'Max':
            mejorValor = -float("inf")
            movimientos = self.movimientos_posibles(nodo.tablero, nodo.jugador)
            for jugada in movimientos:
                if jugada not in movimientos_realizados:
                    movimientos_realizados.add(jugada)
                    nuevoTablero = self.realizarJugada(copy.deepcopy(nodo.tablero), jugada, nodo.jugador)
                    nuevoNodo = Nodo(nuevoTablero, self.oponente(nodo.jugador), nodo.profundidad - 1)
                    valor = self.minimax(nuevoNodo, alfa, beta, movimientos_realizados)
                    mejorValor = max(mejorValor, valor)
                    alfa = max(alfa, mejorValor)
                    movimientos_realizados.remove(jugada)
                    if beta <= alfa:
                        break  # Corte alfa-beta
            return mejorValor
        else:
            peorValor = float("inf")
            movimientos = self.movimientos_posibles(nodo.tablero, nodo.jugador)
            for jugada in movimientos:
                if jugada not in movimientos_realizados:
                    movimientos_realizados.add(jugada)
                    nuevoTablero = self.realizarJugada(copy.deepcopy(nodo.tablero), jugada, nodo.jugador)
                    nuevoNodo = Nodo(nuevoTablero, self.oponente(nodo.jugador), nodo.profundidad - 1)
                    valor = self.minimax(nuevoNodo, alfa, beta, movimientos_realizados)
                    peorValor = min(peorValor, valor)
                    beta = min(beta, peorValor)
                    movimientos_realizados.remove(jugada)
                    if beta <= alfa:
                        break  # Corte alfa-beta
            return peorValor

def verificar_primer_movimiento_max(tablero, profundidad, jugador, movimientos_realizados):
    juego = Juego()
    movimientos_iniciales = juego.movimientos_posibles(tablero, jugador)
    mejor_utilidad = -float('inf')
    alfa = -float("inf")
    beta = float("inf")
    mejor_movimiento = None

    for movimiento in movimientos_iniciales:
        movimientos_realizados.add(movimiento)  # Agregar movimiento al registro
        nuevo_tablero = juego.realizarJugada(copy.deepcopy(tablero), movimiento, jugador)
        nuevo_nodo = Nodo(nuevo_tablero, juego.oponente(jugador), profundidad)
        utilidad = juego.minimax(nuevo_nodo, alfa, beta, movimientos_realizados)
        if utilidad > mejor_utilidad:
            mejor_utilidad = utilidad
            mejor_movimiento = movimiento
        movimientos_realizados.remove(movimiento)  # Eliminar movimiento del registro

    return mejor_movimiento
