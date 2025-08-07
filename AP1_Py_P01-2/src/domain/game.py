from .entities.level import Level, ActionResult
from .entities.characters import Player
from .services.utils import *
import data_layer.storage

class Game:
    level: Level

    def __init__(self):
        self.level = Level(Player(100, 20, 20))
        self.invent_state = False
        self.running = True
        self.win = False

    def get_game_info(self):
        player = self.level.player
        walls = self.level.player.seen_walls
        entities = self.level.player.entities
        text_status = self.level.text_status
        win = self.win
        running = self.running
        return {'player': player, 'walls': walls, 'entities': entities, 'invent_state': self.invent_state,
                'text_status': text_status, 'win': win, 'running': running}

    def make_action(self, action: Action):
        if not self.invent_state:
            if action == Action.MOVE_UP:
                result = self.level.move_player(Direction.TOP)
            elif action == Action.MOVE_DOWN:
                result = self.level.move_player(Direction.BOTTOM)
            elif action == Action.MOVE_LEFT:
                result = self.level.move_player(Direction.LEFT)
            elif action == Action.MOVE_RIGHT:
                result = self.level.move_player(Direction.RIGHT)
            else:
                result = None
        else:
            if action == Action.MOVE_UP:
                self.level.player.inventory.selected_itemtype_id = (self.level.player.inventory.selected_itemtype_id - 1)%\
                                                               len(self.level.player.inventory.items)
            elif action == Action.MOVE_DOWN:
                self.level.player.inventory.selected_itemtype_id = (self.level.player.inventory.selected_itemtype_id + 1) % \
                                                         len(self.level.player.inventory.items)
            elif (action != None and 48 <= action <= 57):
                self.level.player.inventory.use_item(action - 48)
            result = None
        if action == Action.FINISH_GAME:
            self.quit()
        if action == Action.INVENT:
            self.invent_state = (1 + self.invent_state) % 2
        self.process_action(result)

    def enemy_move(self):
        result = self.level.move_enemy()

        self.process_action(result)

    def process_action(self, result: ActionResult):
        if result == ActionResult.PLAYER_DEAD:
            self.win = False
            self.running = False
        elif result == ActionResult.NEXT_LEVEL:
            self.go_to_next_level()

    def restart_game(self):
        self.level = Level()

    def quit(self):
        self.save()
        self.running = False

    def go_to_next_level(self):
        if self.level.level_number > 21:
            self.win = True
            self.running = False
        else:
            self.level = Level(self.level.player, self.level.level_number + 1)
        self.save()
    def save(self):
        data_layer.storage.save_progress(self)


