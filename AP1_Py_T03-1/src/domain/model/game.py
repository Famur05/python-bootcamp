import uuid
from domain.model.game_field import GameField

class Game:
    def __init__(self, id=None, game_field: GameField=None):
        self.id = id if id else str(uuid.uuid4())
        self.game_field = game_field
    
    def get_id(self):
        return self.id
    
    def get_game_field(self):
        return self.game_field
    
    def set_game_field(self, game_field):
        self.game_field = game_field