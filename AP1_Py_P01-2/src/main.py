
from domain.game import Game
from presentation.controller import Controller
import data_layer.storage
def main():
    game = data_layer.storage.load_progress()
    if (game == None):
        game = Game()
    control = Controller(game=game)
    control.run()


if __name__ == '__main__':
    main()
