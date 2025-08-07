ROOM_NUMBER_W = 3
ROOM_NUMBER_H = 3

ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 14

SECTION_SIZE = 22

SECTION_PADDING = 4


class Pixel:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"

    def __eq__(self, other):
        if isinstance(other, Pixel):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __sub__(self, other):
        if isinstance(other, Pixel):
            return Pixel(self.x - other.x, self.y - other.y)
        raise TypeError(f"Unsupported operand type(s) for -: 'Pixel' and '{type(other).__name__}'")

    def __add__(self, other):
        if isinstance(other, Pixel):
            return Pixel(self.x + other.x, self.y + other.y)
        raise TypeError(f"Unsupported operand type(s) for +: 'Pixel' and '{type(other).__name__}'")

    def __lt__(self, other):
        if isinstance(other, Pixel):
            return (self.x, self.y) < (other.x, other.y)
        raise TypeError(f"Cannot compare 'Pixel' with '{type(other).__name__}'")

    def __gt__(self, other):
        if isinstance(other, Pixel):
            return (self.x, self.y) > (other.x, other.y)
        raise TypeError(f"Cannot compare 'Pixel' with '{type(other).__name__}'")


class Direction:
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Action:
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    FINISH_GAME = 4
    INVENT = 5


class LocType:
    CORRIDOR_PATH = 0
    CORRIDOR_WALL = 1
    DOOR = 2
    ROOM = 3
    ROOM_WALL = 4


class BattleRes:
    KILLED = 0
    DEAD = 1
