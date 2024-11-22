import numpy as np
import random
from typing import List, Tuple, Optional

class SmartHorsesGame:
    def __init__(self):
        # Tamaño del tablero
        self.board_size = 8
        
       # Generar tablero con colocación no superpuesta
        self.points_board, self.x2_board, self.horse1_pos, self.horse2_pos = self.generar_tablero()
        
        # Puntuaciones de los caballos
        self.horse1_score = 0
        self.horse2_score = 0
        
        # Estado de símbolos x2
        self.horse1_x2 = False
        self.horse2_x2 = False

        # Añadir un nuevo atributo para almacenar el último movimiento
        self.horse2_last_move = None
        
        # Movimientos válidos de caballo de ajedrez
        self.horse_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def generar_tablero(self) -> Tuple[np.ndarray, np.ndarray, Tuple[int, int], Tuple[int, int]]:
        # Inicializar tableros
        points_board = np.zeros((self.board_size, self.board_size), dtype=int)
        x2_board = np.zeros((self.board_size, self.board_size), dtype=bool)
        
        # Generar posiciones disponibles
        all_positions = [
            (x, y) for x in range(self.board_size) 
            for y in range(self.board_size)
        ]

        # Posiciones de los caballos
        horse1_pos = random.sample(all_positions, 1)[0]  # Posición aleatoria para el caballo 1
        all_positions.remove(horse1_pos) # Eliminar posiciones de caballo 1

        horse2_pos = random.sample(all_positions, 1)[0] # Posición aleatoria para el caballo 2
        all_positions.remove(horse2_pos) # Eliminar posiciones de caballo 2
        
        # Generar casillas de puntos
        point_positions = random.sample(all_positions, 10)
        for i, (x, y) in enumerate(point_positions, 1):
            points_board[x, y] = i
            all_positions.remove((x, y))
        
        # Generar símbolos x2
        x2_positions = random.sample(all_positions, 4)
        for x, y in x2_positions:
            x2_board[x, y] = True
        
        return points_board, x2_board, horse1_pos, horse2_pos
    
    def obtener_tablero(self) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
        # Crear una copia del tablero de puntos
        board = self.points_board.copy()
        
        # Marcar las casillas x2 con -1 en el tablero
        board[self.x2_board] = -1
        
        # Marcar las posiciones de los caballos
        # Usamos -2 para el caballo 1 y -3 para el caballo 2
        board[self.horse1_pos] = -2
        board[self.horse2_pos] = -3
        
        return board, self.horse1_pos, self.horse2_pos

    def movimiento_valido(self, current_pos: Tuple[int, int], next_pos: Tuple[int, int], horse: int) -> bool:
        x1, y1 = current_pos
        x2, y2 = next_pos
        
        # Verificar movimiento de caballo de ajedrez
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        move_valid = (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
        
        # Verificar que esté dentro del tablero
        in_board = (0 <= x2 < self.board_size and 0 <= y2 < self.board_size)
        
        # Verificar que no colisione con la posición del otro caballo
        if horse == 1:
            horse_other_pos = self.horse2_pos
        else:
            horse_other_pos = self.horse1_pos
        
        not_colliding = next_pos != horse_other_pos
        
        return move_valid and in_board and not_colliding

    def obtener_movimientos_validos(self, current_pos: Tuple[int, int], horse: int) -> List[Tuple[int, int]]:
        x, y = current_pos
        moves = []
        
        for dx, dy in self.horse_moves:
            next_pos = (x + dx, y + dy)
            if self.movimiento_valido(current_pos, next_pos, horse):
                moves.append(next_pos)
        
        return moves

    def mover(self, horse: int, move: Tuple[int, int]) -> None:
        """Realiza un movimiento para un caballo"""
        if horse == 1:
            current_pos = self.horse1_pos
            current_x2 = self.horse1_x2
            current_score = self.horse1_score
        else:
            current_pos = self.horse2_pos
            current_x2 = self.horse2_x2
            current_score = self.horse2_score

        # Añadir puntos de la casilla
        points = self.points_board[move[0], move[1]]
        
        # Aplicar multiplicador x2 si está presente
        if self.x2_board[move[0], move[1]] and not current_x2:
            current_x2 = True
        elif current_x2 and points > 0:
            points *= 2
            current_x2 = False

        # Actualizar puntaje y posición
        current_score += points
        
        # Limpiar la casilla de puntos y x2
        self.points_board[move[0], move[1]] = 0
        self.x2_board[move[0], move[1]] = False

        # Actualizar estado del caballo
        if horse == 1:
            self.horse1_pos = move
            self.horse1_score = current_score
            self.horse1_x2 = current_x2
        else:
            self.horse2_pos = move
            self.horse2_score = current_score
            self.horse2_x2 = current_x2
            self.horse2_last_move = move

    def game_over(self) -> bool:
        """Verifica si quedan casillas con puntos"""
        return np.all(self.points_board == 0)

    def minimax(self, depth: int, maximizing_player: bool, horse: int) -> Tuple[Optional[Tuple[int, int]], int]:
        if depth == 0 or self.game_over():
            # Evaluar el estado del juego
            return None, self.evaluar_tablero(horse)

        # Determinar la posición actual y los movimientos válidos
        if horse == 1:
            current_pos = self.horse1_pos
        else:
            current_pos = self.horse2_pos

        valid_moves = self.obtener_movimientos_validos(current_pos, horse)

        if len(valid_moves) == 0:
            return None, self.evaluar_tablero(horse)

        # Lógica original de minimax para el caballo 2 o movimientos del caballo 1 sin puntos
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                # Simular el movimiento
                game_copy = self.copy()
                game_copy.mover(horse, move)
                
                # Llamada recursiva al minimax
                _, eval_score = game_copy.minimax(
                    depth - 1, 
                    False, 
                    2 if horse == 1 else 1
                )
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                # Simular el movimiento
                game_copy = self.copy()
                game_copy.mover(horse, move)
                
                # Llamada recursiva al minimax
                _, eval_score = game_copy.minimax(
                    depth - 1, 
                    True, 
                    2 if horse == 1 else 1
                )
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            
            return best_move, min_eval

    def evaluar_tablero(self, horse: int) -> int:
        if horse == 1:
            # Función de utilidad original para el caballo 1: diferencia de puntuaciones
            return self.horse1_score - self.horse2_score
        else:
            # Nueva función de utilidad para el caballo 2
            return self.evaluar_tablero_horse2()
        
    def evaluar_tablero_horse2(self) -> int:
        # Diferencia de puntuaciones base
        score_diff = self.horse2_score - self.horse1_score

        # Localizar posición actual del caballo 2
        x2, y2 = self.horse2_pos

        # Factor de distancia a puntos
        points_distance = self.calcular_distancia(self.horse2_pos)

        # Factor de proximidad a símbolos x2
        x2_proximity = self.calcular_distancia_x2(self.horse2_pos)

        # Ponderación de los factores
        # Ajustar estos pesos permite modificar el comportamiento estratégico
        weights = {
            'score_diff': 5.0,     # Importancia de la diferencia de puntuación
            'points_distance': 5.0,  # Preferir estar cerca de puntos (negativo porque queremos minimizar la distancia)
            'x2_proximity': 1.0,   # Valor de estar cerca de símbolos x2
        }

        # Calcular utilidad ponderada
        utility = (
            weights['score_diff'] * score_diff +
            weights['points_distance'] * points_distance +
            weights['x2_proximity'] * x2_proximity
        )

        return utility
    
    def calcular_distancia(self, pos: Tuple[int, int]) -> float:
        x, y = pos
        point_positions = np.argwhere(self.points_board > 0)
        
        if len(point_positions) == 0:
            return 0  # No hay puntos restantes
        
        # Calcular distancia de Manhattan a los puntos más cercanos
        distances = [abs(x - px) + abs(y - py) for px, py in point_positions]
        return min(distances)

    def calcular_distancia_x2(self, pos: Tuple[int, int]) -> float:
        x, y = pos
        x2_positions = np.argwhere(self.x2_board)
        
        if len(x2_positions) == 0 or self.horse2_x2:
            return 0  # No hay símbolos x2 o ya se tiene uno
        
        # Calcular distancia de Manhattan a los símbolos x2
        distances = [abs(x - px) + abs(y - py) for px, py in x2_positions]
        return -min(distances)  # Negativo para favorecer proximidad
        
    def copy(self):
        game_copy = SmartHorsesGame()
        game_copy.points_board = self.points_board.copy()
        game_copy.x2_board = self.x2_board.copy()
        game_copy.horse1_pos = self.horse1_pos
        game_copy.horse2_pos = self.horse2_pos
        game_copy.horse1_score = self.horse1_score
        game_copy.horse2_score = self.horse2_score
        game_copy.horse1_x2 = self.horse1_x2
        game_copy.horse2_x2 = self.horse2_x2
        game_copy.horse2_last_move = self.horse2_last_move
        return game_copy