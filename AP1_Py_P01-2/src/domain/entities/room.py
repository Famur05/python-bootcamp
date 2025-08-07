import random

from ..services.utils import *


class Room:
    location: Pixel
    width: int
    height: int
    starting_room: bool
    walls: list[Pixel]
    empty: list[Pixel]
    occupied: list[Pixel]
    doors: list[Pixel]
    index: int

    def __init__(self, location: Pixel, index: int):
        self.width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        self.height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

        self.index = index

        dx = random.randint(1, SECTION_SIZE - self.width - SECTION_PADDING - 1)
        dy = random.randint(1, SECTION_SIZE - self.height - SECTION_PADDING - 1)

        self.location = location + Pixel(dx, dy)

        self.starting_room = False

        self.build_walls()

    def occupy_random_location(self):
        location = random.choice(self.empty)
        self.occupied.append(location)
        self.empty.remove(location)
        return location

    def free_occupied_location(self, location: Pixel):
        try:
            self.occupied.remove(location)
            self.empty.append(location)
        except ValueError:
            pass

    def build_walls(self):
        self.walls = []
        self.doors = []
        self.occupied = []
        self.empty = []

        for h in range(self.height):
            for w in range(self.width):
                if not (0 < h < self.height - 1 and 0 < w < self.width - 1):
                    self.walls.append(self.location + Pixel(w, h))
                else:
                    self.empty.append(self.location + Pixel(w, h))

    def build_door(self, door: Pixel):
        self.doors.append(door)
        self.walls.remove(door)