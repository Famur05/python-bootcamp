from .renderer import View
from domain.game import Game


class Controller:
    view: View
    game: Game

    def __init__(self, game: Game):
        self.view = View()
        self.game = game

    def run(self):
        while self.game.running:
            self.view.update(self.game.get_game_info())

            action = self.view.get_user_input()

            self.game.make_action(action)

            self.view.update(self.game.get_game_info())

            self.game.enemy_move()
