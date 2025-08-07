from domain.service.game_service_interface import GameServiceInterface

class GameModule:
    def __init__(self, game_service: GameServiceInterface):
        self.game_service = game_service
    
    def process_move(self, old_game, updated_game):
        if not self.game_service.validate_game_field(old_game, updated_game):
            raise ValueError("Invalid move: previous moves were modified")
        
        game_status = self.game_service.check_game_over(updated_game)
        if game_status != 0:
            return updated_game, game_status
        
        # Получаем ход компьютера
        computer_move = self.game_service.get_next_move(updated_game)
        
        # Проверяем статус игры после хода компьютера
        game_status = self.game_service.check_game_over(computer_move)
        
        return computer_move, game_status
        