import random

from .room import Room
from .items import *
from .corridor import Corridor, Pixel
from .characters import Player, Zombie, Vampire, Ghost, Ogre, Snake
from ..services.utils import *


class ActionResult:
    PLAYER_DEAD = 0
    NEXT_LEVEL = 1


class WayOut:
    location: Pixel

    def __init__(self, location: Pixel):
        self.location = location

    def __str__(self):
        return "<>"


class Level:
    player: Player
    level_number: int
    rooms: list[Room]
    corridors: list[Corridor]
    way_out: WayOut
    enemies: list
    rooms_connected: bool
    items: list[Items]
    text_status: str

    def __init__(self, player: Player, level_number: int = 1):
        self.level_number = level_number

        self.player = player

        self.rooms_connected = False

        self.text_status = f"Welcome to Level {self.level_number}"

        while not self.rooms_connected:
            self.generate_rooms()
            self.build_corridors()
            self.check_connection()

        self.spawn_player()

        self.spawn_way_out()

        self.spawn_enemies()

        self.spawn_items()

    def generate_rooms(self):
        self.rooms = []

        for h in range(ROOM_NUMBER_H):
            for w in range(ROOM_NUMBER_W):
                location = Pixel(w * SECTION_SIZE, h * SECTION_SIZE)
                room = Room(location, h * ROOM_NUMBER_W + w)
                self.rooms.append(room)

    def spawn_player(self):
        room = random.choice(self.rooms)

        location = room.occupy_random_location()

        self.player.location = location

        self.player.seen_walls = room.walls

        room.starting_room = True

    def spawn_way_out(self):
        room = random.choice([r for r in self.rooms if r.starting_room is False])
        location = random.choice([i for i in room.empty])
        self.way_out = WayOut(location)

    def get_all_walls(self):
        walls = []

        for room in self.rooms:
            walls += room.walls

        for corridor in self.corridors:
            walls += corridor.walls

        return walls

    def build_corridors(self):
        self.corridors = []

        room_pairs = []

        for i, room in enumerate(self.rooms):
            candidates = []

            for j in (i - 1, i + 1, i - ROOM_NUMBER_W, i + ROOM_NUMBER_W):
                candidate = (min(i, j), max(i, j))
                if 0 <= j <= len(self.rooms) - 1 and candidate not in room_pairs and (candidate[0] % ROOM_NUMBER_W, candidate[1] % ROOM_NUMBER_W) != (ROOM_NUMBER_W - 1, 0):
                    candidates.append(candidate)

            if candidates:
                corridors_to_build = random.sample(candidates, k=len(candidates) - 1)
            else:
                corridors_to_build = []

            for j in corridors_to_build:
                if j[1] - j[0] == 1:
                    direction = Direction.RIGHT
                else:
                    direction = Direction.BOTTOM

                corridor = Corridor(self.rooms[j[0]], self.rooms[j[1]], direction)
                self.corridors.append(corridor)
                room_pairs.append(j)

    def get_all_path(self):
        path = []
        for corridor in self.corridors:
            path += corridor.path
        return path

    def location_type(self, location: Pixel):
        for corridor in self.corridors:
            if location in corridor.path:
                return LocType.CORRIDOR_PATH

            if location in corridor.walls:
                return LocType.CORRIDOR_WALL

            if location in corridor.doors:
                return LocType.DOOR

        for room in self.rooms:
            if location in room.walls:
                return LocType.ROOM_WALL

            if location in room.empty + room.occupied:
                return LocType.ROOM

    def see_new_walls(self, old_location: Pixel, new_location: Pixel, direction: Direction):
        new_walls = []

        old_loc_type = self.location_type(old_location)

        new_loc_type = self.location_type(new_location)

        if new_loc_type == LocType.CORRIDOR_PATH or (new_loc_type == LocType.DOOR and old_loc_type == LocType.ROOM):
            if direction == Direction.LEFT:
                area = [new_location + Pixel(i, j) for i in range(-2, 1) for j in range(-1, 2)]
            elif direction == Direction.RIGHT:
                area = [new_location + Pixel(i, j) for i in range(0, 3) for j in range(-1, 2)]
            elif direction == Direction.TOP:
                area = [new_location + Pixel(i, j) for i in range(-1, 2) for j in range(-2, 1)]
            else:
                area = [new_location + Pixel(i, j) for i in range(-1, 2) for j in range(0, 3)]

            for corridor in self.corridors:
                if new_location in corridor.path + corridor.doors:
                    new_walls = [wall for wall in area if wall in corridor.walls]
                    break

        elif new_loc_type == LocType.ROOM and old_loc_type == LocType.DOOR:
            for room in self.rooms:
                if old_location in room.doors:
                    new_walls = room.walls
                    break

        elif new_loc_type == LocType.DOOR and old_loc_type == LocType.CORRIDOR_PATH:
            for room in self.rooms:
                if new_location in room.doors:
                    break

            k = 0
            while True:
                k += 1

                if direction == Direction.LEFT:
                    area = [new_location + Pixel(i, j) for i in range(-k, -k + 1) for j in range(-k, k + 1)]
                    new_walls += [wall for wall in area if wall in room.walls]
                    if new_location.x - k == room.location.x:
                        break

                elif direction == Direction.RIGHT:
                    area = [new_location + Pixel(i, j) for i in range(k, k + 1) for j in range(-k, k + 1)]
                    new_walls += [wall for wall in area if wall in room.walls]
                    if new_location.x + k == room.location.x + room.width - 1:
                        break

                elif direction == Direction.TOP:
                    area = [new_location + Pixel(i, j) for i in range(-k, k + 1) for j in range(-k, -k + 1)]
                    new_walls += [wall for wall in area if wall in room.walls]
                    if new_location.y - k == room.location.y:
                        break

                else:
                    area = [new_location + Pixel(i, j) for i in range(-k, k + 1) for j in range(k, k + 1)]
                    new_walls += [wall for wall in area if wall in room.walls]
                    if new_location.y + k == room.location.y + room.height - 1:
                        break

        return new_walls

    def check_connection(self):
        pairs = [(corridor.rooms[0].index, corridor.rooms[1].index) for corridor in self.corridors]

        parent = {i: i for i in range(ROOM_NUMBER_W * ROOM_NUMBER_H)}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_y] = root_x

        for a, b in pairs:
            union(a, b)

        roots = {find(x) for x in parent}

        self.rooms_connected = len(roots) == 1

    def spawn_enemies(self):
        self.enemies = []

        for _ in range(round(self.level_number * 1.5)):
            enemy_type = random.choice([Zombie, Vampire, Ghost, Ogre, Snake])

            enemy = enemy_type(self.level_number)

            room = random.choice([r for r in self.rooms if r.starting_room is False])

            location = room.occupy_random_location()

            enemy.location = location

            self.enemies.append(enemy)

    def spawn_items(self):
        self.items = []

        for _ in range(round(self.level_number * 1.5)):
            item_type = random.choice([Food, Weapon, Elixir, Scroll, Treasure])

            item = item_type()

            room = random.choice([r for r in self.rooms if r.starting_room is False])

            location = room.occupy_random_location()

            item.location = location

            self.items.append(item)

    def find_enemy(self, location: Pixel):
        for enemy in self.enemies:
            if enemy.location == location and enemy.is_alive:
                return enemy
        return None

    def find_items(self, location: Pixel):
        for item in self.items:
            if item.location == location:
                return item
        return None

    def find_room(self, location: Pixel):
        for room in self.rooms:
            if location in room.empty + room.occupied:
                return room

        return None

    def move_player(self, direction: Direction):
        old_location = self.player.location

        if direction == Direction.TOP:
            new_location = old_location + Pixel(0, -1)
        elif direction == Direction.BOTTOM:
            new_location = old_location + Pixel(0, 1)
        elif direction == Direction.RIGHT:
            new_location = old_location + Pixel(1, 0)
        else:
            new_location = old_location + Pixel(-1, 0)

        enemy = self.find_enemy(new_location)
        item = self.find_items(new_location)

        if new_location == self.way_out.location:
            return ActionResult.NEXT_LEVEL

        elif enemy:
            attack_res = self.player.attack(enemy)
            self.text_status = attack_res
            if self.player.is_alive:
                self.clean_location(enemy.location)
            else:
                return ActionResult.PLAYER_DEAD

        elif item:
            if (self.player.inventory.add_item(item)):
                room = self.find_room(new_location)
                room.free_occupied_location(new_location)
                self.items.remove(item) ##########
                self.player.move(new_location)
                self.player.entities = self.get_entities(old_location, new_location, direction)

        elif new_location not in self.get_all_walls():
            self.player.move(new_location)
            new_walls = self.see_new_walls(old_location, new_location, direction)
            self.player.add_new_walls(new_walls)
            self.player.entities = self.get_entities(old_location, new_location, direction)


    def move_enemy(self):
        for enemy in self.enemies:
            enemy.action(self)

            if not self.player.is_alive:
                return ActionResult.PLAYER_DEAD

    def clean_location(self, location: Pixel):
        for room in self.rooms:
            room.free_occupied_location(location)

    def get_entities(self, old_location: Pixel, new_location: Pixel, direction: Direction):
        entities = []

        area = []

        old_loc_type = self.location_type(old_location)

        new_loc_type = self.location_type(new_location)

        if new_loc_type in (LocType.CORRIDOR_PATH, LocType.DOOR):
            for corridor in self.corridors:
                if new_location in corridor.path:
                    view_area = [new_location + Pixel(i, j) for i in range(-2, 3) for j in range(-2, 3)]
                    area += [loc for loc in view_area if loc in corridor.path]
                    break

        if new_loc_type == LocType.ROOM:
            for room in self.rooms:
                if new_location in room.empty + room.occupied:
                    area += room.empty + room.occupied
                    break

        if new_loc_type == LocType.DOOR:
            if old_loc_type == LocType.ROOM:
                if direction == Direction.LEFT:
                    direction = Direction.RIGHT
                elif direction == Direction.RIGHT:
                    direction = Direction.LEFT
                elif direction == Direction.TOP:
                    direction = Direction.BOTTOM
                else:
                    direction = Direction.TOP

            for room in self.rooms:
                if new_location in room.doors:
                    break

            k = 0
            while True:
                k += 1

                if direction == Direction.LEFT:
                    view_area = [new_location + Pixel(i, j) for i in range(-k, -k + 1) for j in range(-k, k + 1)]
                    area += [loc for loc in view_area if loc in room.empty + room.occupied]
                    if new_location.x - k == room.location.x:
                        break

                elif direction == Direction.RIGHT:
                    view_area = [new_location + Pixel(i, j) for i in range(k, k + 1) for j in range(-k, k + 1)]
                    area += [loc for loc in view_area if loc in room.empty + room.occupied]
                    if new_location.x + k == room.location.x + room.width - 1:
                        break

                elif direction == Direction.TOP:
                    view_area = [new_location + Pixel(i, j) for i in range(-k, k + 1) for j in range(-k, -k + 1)]
                    area += [loc for loc in view_area if loc in room.empty + room.occupied]
                    if new_location.y - k == room.location.y:
                        break

                else:
                    view_area = [new_location + Pixel(i, j) for i in range(-k, k + 1) for j in range(k, k + 1)]
                    area += [loc for loc in view_area if loc in room.empty + room.occupied]
                    if new_location.y + k == room.location.y + room.height - 1:
                        break

        for enemy in [j for j in self.enemies if j.is_alive is True]:
            if enemy.location in area:
                entities.append(enemy)

        if self.way_out.location in area:
            entities.append(self.way_out)

        for item in self.items:
            if item.location in area:
                entities.append(item)

        return entities
