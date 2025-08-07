from abc import ABC, abstractmethod

class GameRepositoryInterface(ABC):
    @abstractmethod
    def save_game(self, game):
        """
        Сохраняет текущую игру.
        """
        pass
    
    @abstractmethod
    def get_game(self, game_id):
        """
        Получает текущую игру по ID.
        """
        pass