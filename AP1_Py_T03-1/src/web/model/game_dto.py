from web.model.game_field_dto import GameFieldDto

class GameDto:
    def __init__(self, id=None, game_field=None):
        self.id = id
        self.game_field = game_field if game_field else GameFieldDto()
    
    def to_dict(self):
        return {
            "id": self.id,
            "gameField": self.game_field.to_dict()
        }
    
    @staticmethod
    def from_dict(data):
        if not data:
            return None
        
        game_field = GameFieldDto.from_dict(data.get("gameField", {}))
        return GameDto(data.get("id"), game_field)