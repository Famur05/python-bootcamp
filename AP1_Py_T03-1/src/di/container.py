from datasource.repository.game_repository_impl import GameStorage, GameRepositoryImpl
from domain.service.game_service_impl import GameServiceImpl
from web.module.game_module import GameModule
from web.route.game_route import GameRoute

class Container:
    def __init__(self):
        # Singleton для хранилища игр
        self.game_storage = GameStorage()
        
        # Репозиторий для работы с хранилищем
        self.game_repository = GameRepositoryImpl(self.game_storage)
        
        # Сервис для работы с бизнес-логикой
        self.game_service = GameServiceImpl()
        
        # Модуль для обработки игровой логики
        self.game_module = GameModule(self.game_service)
        
        # Маршруты для API
        self.game_route = GameRoute(self.game_module, self.game_repository)