import random
from ..services.utils import *
from ..services.invent import Inventory


class Stat:
    def __init__(self, base_value, max_value=100):
        self.max_value = max_value
        self.base_value = base_value  # Базовое значение
        self.temp_bonus = 0  # Временный бонус
        self.bonus_duration = 0  # Длительность бонуса

    def apply_bonus(self, bonus, duration):
        self.temp_bonus += bonus
        self.bonus_duration = max(self.bonus_duration, duration)

    def update(self):
        if self.bonus_duration > 0:
            self.bonus_duration -= 1
            if self.bonus_duration == 0:
                self.temp_bonus = 0

    def current_value(self):
        return self.base_value + self.temp_bonus

    def decrease(self, value):
        self.base_value -= value


class Character:
    location: Pixel
    # health: Stat  # оно инициализируется уже у игрока.
    # agility: Stat # оно инициализируется уже у игрока. Конечно можно сделтьа
    # strength: Stat
    is_alive: bool

    def __init__(self):
        self.is_alive = True

    def move(self, new_location: Pixel):
        self.location = new_location


    # def attack(self, other):
    #     # бой
    #     other.is_alive = False
    #     self.is_alive = True


class Player(Character):
    seen_walls: list[Pixel]
    entities: list

    def __init__(self, max_health, agility, strength):
        super().__init__()
        self.entities = []
        self.health = Stat(max_health, max_health)  # Здоровье
        self.agility = Stat(agility, 20)  # Ловкость
        self.strength = Stat(strength, 20)  # Сила
        self.total_power = 1  # Мощь
        self.treasure = 0
        self.inventory = Inventory(self) # Рюкзак для предметов
        self.wear_weapon = 0
        self.speed = 1

    def move(self, new_location: Pixel):
        self.location = new_location
        self.update_stats()

    def add_new_walls(self, walls: list[Pixel]):
        if walls:
            self.seen_walls = list(set(self.seen_walls + walls))

    def __repr__(self):
        return "@@"

    def update_stats(self):
        # Обновляем все характеристики
        self.health.update()
        self.agility.update()
        self.strength.update()

    def take_damage(self, damage, game_model):
        effective_damage = max(0, damage - self.agility.current_value())  # Учитываем ловкость
        self.health.base_value -= effective_damage

        if self.health.base_value <= 0:
            game_model.end_game(win=False)

    def collect_treasure(self, amount):
        self.treasure += amount

    def attack(self, other):
        evasion = random.choice(range(self.agility.current_value() + self.speed + other.agility + other.speed))
        if self.agility.current_value() + self.speed >= evasion:
            damage = round(self.total_power * self.strength.current_value(), 2)
            other.health -= damage
            if other.health <= 0:
                other.is_alive = False
            return f"{self.__class__.__name__} damages {other.__class__.__name__} by {damage} points. Remaining health {other.health}"
        else:
            return f"{self.__class__.__name__} attacks, {other.__class__.__name__} evades"
        self.update_stats()




class Enemy(Character):
    health: int
    agility: int  # Ловкость
    strength: int  # Сила
    loot: int
    speed: int = 1
    aggression: int = 1
    name: str

    def __init__(self, health, agility, strength, loot, speed=1, aggression=1):
        super().__init__()
        self.name = self.__class__.__name__
        self.aggression = aggression
        self.loot = loot
        self.target = None
        self.agility = agility
        self.speed = speed
        self.health = health
        self.strength = strength


    def action(self, level):
        player_location = level.player.location

        # Зона атаки (4 соседних клетки)
        attack_zone = [
            self.location + Pixel(i, j)
            for i, j in ((0, 1), (1, 0), (0, -1), (-1, 0))
        ]
        aggression_zone = [
            self.location + Pixel(i, j)
            for i in range(-self.aggression, self.aggression + 1)
            for j in range(-self.aggression, self.aggression + 1)
            if (i, j) != (0, 0)  # Исключаем клетку с самим врагом
        ]

        if self.is_alive and (player_location in attack_zone):
            self.attack(level.player)  # Атакуем, если игрок рядом
        elif player_location in aggression_zone:
            self.haunt_move(player_location, level)  # Преследуем, если игрок в зоне агрессии
        else:
            self.random_move(level)  # Блуждаем, если игрок далеко

    def random_move(self, level):
        # Враг случайно выбирает направление
        move_x = random.choice((-self.speed, 0, self.speed))
        move_y = random.choice((-self.speed, 0, self.speed))

        new_x = self.location.x + move_x
        new_y = self.location.y + move_y

        if self.check_new_location(level, new_x, new_y):
            self.location.x = new_x
            self.location.y = new_y

    def haunt_move(self, player_location, level):
        # Вычисляем вектор движения к игроку
        dx = player_location.x - self.location.x
        dy = player_location.y - self.location.y

        # Определяем направление движения (по горизонтали или вертикали)
        if dx > 0:
            move_x = self.speed
        elif dx < 0:
            move_x = -self.speed
        else:
            move_x = 0

        if dy > 0:
            move_y = self.speed
        elif dy < 0:
            move_y = -self.speed
        else:
            move_y = 0
        # Сначала пробуем двигаться в горизонтальном направлении
        if move_x and self.check_new_location(level, self.location.x + move_x, self.location.y):
            self.location.x += move_x
        # Если горизонтальное движение невозможно, пробуем двигаться вертикально
        elif move_y and self.check_new_location(level, self.location.x, self.location.y + move_y):
            self.location.y += move_y


    def check_new_location(self, level, x, y):
        result = False
        if (level.player.location.x != x and level.player.location.y != y):  # если новая позиция не совпадает с позицией игрока
            for room in level.rooms:  # перебираем комнаты
                for location in room.empty:  # перебираем все свободные точки в комнате
                    if location.x == x and location.y == y:  # если новая позиция в списке свободных
                        result = True  # поднимаем флаг
            for corid in level.corridors:  # перебираем коридоры
                for corid_location in corid.path:  # перебираем точки пути в коридоре
                    if corid_location.x == x and corid_location.y == y:  # если новая позиция в списке путей
                        result = True  # поднимаем флаг
            if result:  # если флаг поднят
                for item in level.items:  # перебираем список предметов
                    if item.location.x == x and item.location.y == y:  # если новая позиция совпадает с положением предмета
                        result = False  # опускаем флаг

        return result  # возвращаем флаг

    def attack(self, other):
        evasion = random.choice(range(self.agility + self.speed + other.agility.current_value() + other.speed))
        if self.agility + self.speed >= evasion:
            damage = self.strength
            other.health.decrease(damage)
            if other.health.current_value() <= 0:
                other.is_alive = False
            return f"{self.__class__.__name__} damages {other.__class__.__name__} by {damage} points"
        else:
            return f"{self.__class__.__name__} attacks, {other.__class__.__name__} evades"




class Zombie(Enemy):
    def __init__(self, level_num):
        super().__init__(health=20 + level_num*2,
                         agility=1 + level_num//5,
                         strength=5 + level_num//3,
                         aggression=2 + level_num//7,
                         loot=20 + level_num*2)

    def __repr__(self):
        return "Zz"

class Vampire(Enemy):
    def __init__(self, level_num):
        super().__init__(health=20 + level_num*2,
                         agility=3 + level_num//5,
                         strength=5 + level_num//3,
                         aggression=3 + level_num//7,
                         loot=40 + level_num*3)

    def __repr__(self):
        return "Vv"

class Ghost(Enemy):
    def __init__(self, level_num):
        self.invisibility = True
        super().__init__(health=5 + level_num*2,
                         agility=3 + level_num//5,
                         strength=2 + level_num//3,
                         aggression=1 + level_num//7,
                         loot=10 + level_num*2)

    def __repr__(self):
        return "Gg"

    def random_move(self, level):
        self.speed = random.randint(1, 4) # случайная скорость
        super().random_move(level)


class Ogre(Enemy):
    def __init__(self, level_num):
        super().__init__(health=30 + level_num*2,
                         agility=1 + level_num//5,
                         strength=6 + level_num//3,
                         aggression=2 + level_num//7,
                         speed=2,
                         loot=50 + level_num*5)

    def __repr__(self):
        return "Oo"

class Snake(Enemy):
    def __init__(self, level_num):
        super().__init__(health=5 + level_num*2,
                         agility=5 + level_num//5,
                         strength=4 + level_num//3,
                         aggression=3 + level_num//7,
                         loot=30 + level_num*3)

    def __repr__(self):
        return "Ss"

    def random_move(self, level):
        step_x = self.location.x + random.choice((-self.speed, self.speed))
        step_y = self.location.y + random.choice((-self.speed, self.speed))
        for _ in range(5):
            step_x = self.location.x + random.choice((-self.speed, self.speed))
            step_y = self.location.y + random.choice((-self.speed, self.speed))
            if self.check_new_location(level, step_x, step_y):
                self.location.x = step_x
                self.location.y = step_y
                break



# class Mimic(Enemy):
#     def __init__(self, level_num):
#         super().__init__(health=20 + level_num*2,
#                          agility=3 + level_num//5,
#                          strength=2 + level_num//3,
#                          aggression=1 + level_num//7,
#                          loot=30 + level_num*3)
