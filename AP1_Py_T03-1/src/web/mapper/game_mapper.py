from domain.model.game import Game
from domain.model.game_field import GameField
from web.model.game_dto import GameDto
from web.model.game_field_dto import GameFieldDto

class GameWebMapper:
    @staticmethod
    def domain_to_dto(game):
        if game is None:
            return None
        
        game_field = game.get_game_field()
        game_field_dto = GameFieldDto(game_field.get_matrix())
        
        return GameDto(game.get_id(), game_field_dto)
    
    @staticmethod
    def dto_to_domain(game_dto):
        if game_dto is None:
            return None
        
        game_field = GameField(game_dto.game_field.matrix)
        
        return Game(game_dto.id, game_field)