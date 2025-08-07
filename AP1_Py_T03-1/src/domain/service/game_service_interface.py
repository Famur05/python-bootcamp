from abc import ABC, abstractmethod

class GameServiceInterface(ABC):
    @abstractmethod
    def get_next_move(self, game):
        """
        Получает следующий ход компьютера используя алгоритм Минимакс.
        """
        pass
    
    @abstractmethod
    def validate_game_field(self, game, updated_game):
        """
        Проверяет, что предыдущие ходы не были изменены.
        """
        pass
    
    @abstractmethod
    def check_game_over(self, game):
        """
        Проверяет, закончилась ли игра (победа, ничья).
        0 - игра продолжается, 1 - победа игрока, 2 - победа компьютера, 3 - ничья
        """
        pass