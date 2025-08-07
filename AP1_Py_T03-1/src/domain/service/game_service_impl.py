from domain.service.game_service_interface import GameServiceInterface
from domain.model.game_field import GameField
from domain.model.game import Game
import copy

class GameServiceImpl(GameServiceInterface):
    def get_next_move(self, game: Game) -> Game:
        game_field: GameField = game.get_game_field()
        matrix = game_field.get_matrix()
        
        if self.check_game_over(game) != 0:
            return game
        
        best_score = float('-inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == 0:
                    matrix[i][j] = 2 
                    score = self.minimax(matrix, 0, False)
                    matrix[i][j] = 0
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            matrix[best_move[0]][best_move[1]] = 2
            updated_game_field = GameField(matrix)
            updated_game = Game(game.get_id(), updated_game_field)
            return updated_game
        
        return game
    
    def minimax(self, matrix, depth, is_maximizing):
        temp_game = Game(None, GameField(matrix))
        result = self.check_game_over(temp_game)
        
        if result == 2:  # Компьютер победил
            return 10 - depth
        elif result == 1:  # Игрок победил
            return depth - 10
        elif result == 3:  # Ничья
            return 0
        
        if is_maximizing:  # Ход компьютера (максимизируем)
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if matrix[i][j] == 0:
                        matrix[i][j] = 2
                        score = self.minimax(matrix, depth + 1, False)
                        matrix[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:  # Ход игрока (минимизируем)
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if matrix[i][j] == 0:
                        matrix[i][j] = 1
                        score = self.minimax(matrix, depth + 1, True)
                        matrix[i][j] = 0
                        best_score = min(score, best_score)
            return best_score
    
    def validate_game_field(self, old_game, updated_game):
        """
        Проверяет, что предыдущие ходы не были изменены.
        """
        old_matrix = old_game.get_game_field().get_matrix()
        new_matrix = updated_game.get_game_field().get_matrix()

        for i in range(3):
            for j in range(3):
                if old_matrix[i][j] != 0 and old_matrix[i][j] != new_matrix[i][j]:
                    return False
        
        x_count_old = sum(row.count(1) for row in old_matrix)
        x_count_new = sum(row.count(1) for row in new_matrix)
        
        return x_count_new == x_count_old + 1
    
    def check_game_over(self, game: Game) -> int:
        """
        0 - игра продолжается, 1 - победа игрока, 2 - победа компьютера, 3 - ничья
        """
        matrix = game.get_game_field().get_matrix()
        
        for i in range(3):
            if matrix[i][0] == matrix[i][1] == matrix[i][2] != 0:
                return matrix[i][0]
            
        for i in range(3):
            if matrix[0][i] == matrix[1][i] == matrix[2][i] != 0:
                return matrix[0][i]

        if matrix[0][0] == matrix[1][1] == matrix[2][2] != 0:
            return matrix[0][0]
        if matrix[0][2] == matrix[1][1] == matrix[2][0] != 0:
            return matrix[0][2]

        for i in range(3):
            for j in range(3):
                if matrix[i][j] == 0:
                    return 0
        
        return 3
    