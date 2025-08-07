from datasource.repository.game_repository_interface import GameRepositoryInterface
from datasource.mapper.game_mapper import GameMapper
from datasource.model.game_entity import GameEntity
import threading

class GameStorage:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GameStorage, cls).__new__(cls)
                cls._instance.games = {}
        return cls._instance
    
    def save_game(self, game_entity: GameEntity):
        with self._lock:
            self.games[game_entity.id] = game_entity
    
    def get_game(self, game_id):
        with self._lock:
            return self.games.get(game_id)

class GameRepositoryImpl(GameRepositoryInterface):
    def __init__(self, game_storage: GameStorage):
        self.game_storage = game_storage
    
    def save_game(self, game):
        game_entity: GameEntity = GameMapper.domain_to_entity(game)
        self.game_storage.save_game(game_entity)
        return game
    
    def get_game(self, game_id):
        game_entity = self.game_storage.get_game(game_id)
        return GameMapper.entity_to_domain(game_entity)