import random

from ..services.utils import *
from .room import Room


class Corridor:
    walls: list[Pixel]
    path: list[Pixel]
    doors: list[Pixel]
    rooms: list[Room]
    direction: Direction

    def __init__(self, room_a: Room, room_b: Room, direction: Direction):
        self.walls = []
        self.path = []
        self.doors = []
        self.rooms = [room_a, room_b]
        self.direction = direction

        self.build_doors()

        self.build_path()

    def build_doors(self):
        room_a = self.rooms[0]
        room_b = self.rooms[1]

        if self.direction == Direction.RIGHT:
            door_a = room_a.location + Pixel(room_a.width - 1, random.randint(1, room_a.height - 2))
            door_b = room_b.location + Pixel(0, random.randint(1, room_b.height - 2))
        else:
            door_a = room_a.location + Pixel(random.randint(1, room_a.width - 2), room_a.height - 1)
            door_b = room_b.location + Pixel(random.randint(1, room_b.width - 2), 0)

        room_a.build_door(door_a)
        room_b.build_door(door_b)

        self.doors.append(door_a)
        self.doors.append(door_b)

    def build_path(self):
        if self.direction == Direction.RIGHT:
            self.build_path_right()
        else:
            self.build_path_bottom()

    def build_path_right(self):
        door_a = self.doors[0]
        door_b = self.doors[1]

        cur_path = door_a

        while cur_path != door_b:
            cur_path = cur_path + Pixel(1, 0)

            self.path.append(cur_path)

            self.walls += [cur_path + Pixel(0, 1), cur_path + Pixel(0, -1)]

            if cur_path.x == (door_a.x + door_b.x) // 2:
                diff = door_b.y - door_a.y
                sign = 0

                if diff:
                    sign = int(diff / abs(diff))
                    self.walls.remove(cur_path + Pixel(0, sign))
                    self.walls += [cur_path + Pixel(1, 0), cur_path + Pixel(1, - sign)]

                for i in range(abs(diff)):
                    cur_path = cur_path + Pixel(0, sign)
                    self.path.append(cur_path)
                    self.walls += [cur_path + Pixel(1, 0), cur_path + Pixel(-1, 0)]

                if diff:
                    self.walls += [cur_path + Pixel(0, sign), cur_path + Pixel(-1, sign)]
                    self.walls.remove(cur_path + Pixel(1, 0))

        self.path.pop()

    def build_path_bottom(self):
        door_a = self.doors[0]
        door_b = self.doors[1]

        cur_path = door_a

        while cur_path != door_b:
            cur_path = cur_path + Pixel(0, 1)

            self.path.append(cur_path)

            self.walls += [cur_path + Pixel(1, 0), cur_path + Pixel(-1, 0)]

            if cur_path.y == (door_a.y + door_b.y) // 2:
                diff = door_b.x - door_a.x
                sign = 0

                if diff:
                    sign = int(diff / abs(diff))
                    self.walls.remove(cur_path + Pixel(sign, 0))
                    self.walls += [cur_path + Pixel(0, 1), cur_path + Pixel(-sign, 1)]

                for i in range(abs(diff)):
                    cur_path = cur_path + Pixel(sign, 0)
                    self.path.append(cur_path)
                    self.walls += [cur_path + Pixel(0, 1), cur_path + Pixel(0, -1)]

                if diff:
                    self.walls += [cur_path + Pixel(sign, 0), cur_path + Pixel(sign, -1)]

                    self.walls.remove(cur_path + Pixel(0, 1))

        self.path.pop()

