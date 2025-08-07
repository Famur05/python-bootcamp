from domain.model.game import Game
from domain.model.game_field import GameField
from datasource.model.game_entity import GameEntity
from datasource.model.game_field_entity import GameFieldEntity

class GameMapper:
    @staticmethod
    def domain_to_entity(game: Game):
        if game is None:
            return None
        
        game_field = game.get_game_field()
        game_field_entity = GameFieldEntity(game_field.get_matrix())
        
        return GameEntity(game.get_id(), game_field_entity)
    
    @staticmethod
    def entity_to_domain(game_entity):
        if game_entity is None:
            return None
        
        game_field = GameField(game_entity.game_field.matrix)
        
        return Game(game_entity.id, game_field)