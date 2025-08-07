import curses
from domain.services.utils import *

TEXT_SECTION_WIDTH = 80


class View:
    window_h: int = ROOM_NUMBER_H * SECTION_SIZE + 2
    window_w: int = ROOM_NUMBER_W * SECTION_SIZE * 2 + TEXT_SECTION_WIDTH

    def __init__(self):
        curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.window = curses.newwin(self.window_h, self.window_w, 0, 0)
        self.window.keypad(True)

    def update(self, game_info):
        self.window.clear()
        if(game_info['running']):
            if not game_info['invent_state']:
                for i in game_info['walls']:
                    self.window.addstr(i.y, 2 * i.x, '[]')

                self.window.addstr(game_info['player'].location.y, 2 * game_info['player'].location.x, str(game_info['player']))

                for entity in game_info['entities']:
                    self.window.addstr(entity.location.y, 2 * entity.location.x, str(entity))
            else:
                self.window.addstr(15, 50, str(game_info['player'].inventory))

            self.window.addstr(5, self.window_w - TEXT_SECTION_WIDTH + 3, game_info['text_status'])
            self.window.addstr(7, self.window_w - TEXT_SECTION_WIDTH + 3, 'Player:')
            player_info = f"""HEALTH {game_info['player'].health.current_value()}  AGILITY {game_info['player'].agility.current_value()} STRENGTH {game_info['player'].strength.current_value()} TOTAL POWER {game_info['player'].total_power * game_info['player'].strength.current_value()} SCORE {game_info['player'].treasure}"""
            self.window.addstr(9, self.window_w - TEXT_SECTION_WIDTH + 3, player_info)

            for i in range(self.window_w - 1):
                for j in range(self.window_h - 1):
                    if (i, j) in ((0, 0), (self.window_w - TEXT_SECTION_WIDTH, self.window_h - 2), (0, self.window_h - 2), (self.window_w - TEXT_SECTION_WIDTH, 0)):
                        self.window.addstr(j, i, 'o')

                    elif i in (0, self.window_w - TEXT_SECTION_WIDTH):
                        self.window.addstr(j, i, '|')

                    elif j in (0, self.window_h - 2) and i < (self.window_w - TEXT_SECTION_WIDTH):
                        self.window.addstr(j, i, '-')
        else:
            if game_info['win']:
                print("Поздравляем! Вы прошли игру!")
            else:
                print("Игра окончена. Попробуйте снова.")
        self.window.refresh()

    def get_user_input(self):
        key = self.window.getch()

        if key == curses.KEY_UP:
            return Action.MOVE_UP
        elif key == curses.KEY_DOWN:
            return Action.MOVE_DOWN
        elif key == curses.KEY_RIGHT:
            return Action.MOVE_RIGHT
        elif key == curses.KEY_LEFT:
            return Action.MOVE_LEFT
        elif key == ord('i'):
            return Action.INVENT
        elif 48 <= key <= 57:
            return key
        elif key == ord('q'):
            return Action.FINISH_GAME