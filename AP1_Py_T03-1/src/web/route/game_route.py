from flask import Blueprint, request, jsonify
from web.mapper.game_mapper import GameWebMapper
from web.model.game_dto import GameDto

game_blueprint = Blueprint('game', __name__)

class GameRoute:
    def __init__(self, game_module, game_repository):
        self.game_module = game_module
        self.game_repository = game_repository
        
        # Регистрация маршрутов
        game_blueprint.route('/<game_id>', methods=['POST'])(self.make_move)
        game_blueprint.route('/new', methods=['GET'])(self.new_game)
    
    def make_move(self, game_id):
        try:
            # Получаем текущую игру из репозитория
            current_game = self.game_repository.get_game(game_id)
            if not current_game:
                return jsonify({"error": "Game not found"}), 404
            
            # Получаем обновленную игру от пользователя
            data = request.json
            updated_game_dto = GameDto.from_dict(data)
            updated_game = GameWebMapper.dto_to_domain(updated_game_dto)
            
            # Обрабатываем ход
            computer_move, game_status = self.game_module.process_move(current_game, updated_game)
            
            # Сохраняем обновленную игру
            self.game_repository.save_game(computer_move)
            
            # Преобразуем результат в DTO
            result_dto = GameWebMapper.domain_to_dto(computer_move)
            result = result_dto.to_dict()
            
            # Добавляем статус игры в ответ
            result["status"] = game_status
            
            return jsonify(result)
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal server error: " + str(e)}), 500
    
    def new_game(self):
        try:
            # Создаем новую игру
            from domain.model.game import Game
            from domain.model.game_field import GameField
            
            new_game = Game(None, GameField())
            saved_game = self.game_repository.save_game(new_game)
            
            # Преобразуем результат в DTO
            result_dto = GameWebMapper.domain_to_dto(saved_game)
            
            return jsonify(result_dto.to_dict())
            
        except Exception as e:
            return jsonify({"error": "Internal server error: " + str(e)}), 500