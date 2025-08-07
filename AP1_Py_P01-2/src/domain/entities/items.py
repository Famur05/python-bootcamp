import random
from typing import Optional
from ..services.utils import *

# Глобальные переменные для типов и подтипов предметов
ITEM_TYPES = ["food", "weapon", "scroll", "treasure", "elixir", "none"]

# Класс для хранения списков подтипов
class ItemSubtypes:
    FOOD = ["apple", "bread", "potato"]
    WEAPON = ["sword", "mace", "dagger"]
    ELIXIR = ["agility elixir", "strength elixir", "health elixir", "time elixir"]
    SCROLL = ["agility scroll", "strength scroll", "health scroll"]
    TREASURE = ["diamonds", "gold relique", "rare stones", "gold skull"]

# Базовый класс для всех предметов
class Items:
    location: Pixel
    def __init__(self, item_type: str, subtype: str):
        self.type = item_type
        self.subtype = subtype


    def use(self, character) -> bool:
        """
        Использование предмета. Возвращает True, если предмет был использован.
        """
        raise NotImplementedError("Метод use должен быть переопределен в подклассе")


# Класс для еды
class Food(Items):
    def __init__(self):
        super().__init__("food", random.choice(ItemSubtypes.FOOD))
        self.health_bonus = random.randint(10, 40)

    def use(self, character) -> bool:
        character.health.base_value = min(
            character.health.max_value,
            character.health.base_value + self.health_bonus
        )
        return True

    def __repr__(self):
        return "()"

    def get_info(self):
        return f"{self.subtype}; bonus: {self.health_bonus}"

# Класс для оружия
class Weapon(Items):
    def __init__(self, max_power: float = 2):
        super().__init__("weapon", random.choice(ItemSubtypes.WEAPON))
        self.power = random.uniform(max_power - 1, max_power)
        self.active = 0

    def use(self, character) -> bool:
        # Оружее можно экипировать, только если у перса не надето сейчас,
        # Если надето, то ничего не происходит,
        # но если мы пытаемся использовать надетый предмет, он снимает
        # и мы можем надеть другой
        if(character.wear_weapon == 0):
            character.total_power *= self.power
            self.active = 1
            character.wear_weapon = 1
        elif(self.active):
            character.total_power = 1
            self.active = 0
            character.wear_weapon = 0

        return False

    def __repr__(self):
        return "-+"

    def get_info(self):
        return f"{self.subtype}; power: {self.power}; active: {'yes' if self.active else 'no'}"

# Класс для эликсиров
class Elixir(Items):
    def __init__(self):
        super().__init__("elixir", random.choice(ItemSubtypes.ELIXIR))
        self.duration = random.randint(5, 20)
        self._initialize_effect()

    def _initialize_effect(self):
        if self.subtype == "agility elixir":
            self.bonus = random.randint(10, 20)
            self.stat = "agility"
        elif self.subtype == "strength elixir":
            self.bonus = random.randint(20, 30)
            self.stat = "strength"
        elif self.subtype == "health elixir":
            self.bonus = random.randint(50, 100)
            self.stat = "health"
        elif self.subtype == "time elixir":
            self.duration += random.randint(5, 20)
            self.bonus = 0
            self.stat = None

    def use(self, character) -> bool:
        if self.stat:
            stat = getattr(character, self.stat)
            stat.apply_bonus(self.bonus, self.duration)
        return True

    def __repr__(self):
        return "=|"

    def get_info(self):
        return f"{self.subtype}; bonus: {self.bonus}; duration: {self.duration}"

# Класс для свитков
class Scroll(Items):
    def __init__(self):
        super().__init__("scroll", random.choice(ItemSubtypes.SCROLL))
        self._initialize_effect()

    def _initialize_effect(self):
        if self.subtype == "agility scroll":
            self.bonus = random.randint(1, 5)
            self.stat = "agility"
        elif self.subtype == "strength scroll":
            self.bonus = random.randint(5, 10)
            self.stat = "strength"
        elif self.subtype == "health scroll":
            self.bonus = random.randint(20, 50)
            self.stat = "health"

    def use(self, character) -> bool:
        if self.stat:
            stat = getattr(character, self.stat)
            stat.base_value += self.bonus
        return True

    def __repr__(self):
        return "{}"

    def get_info(self):
        return f"{self.subtype}; bonus: {self.bonus};"

# Класс для сокровищ
class Treasure(Items):
    def __init__(self):
        super().__init__("treasure", random.choice(ItemSubtypes.TREASURE))
        self.cost = random.randint(10, 100)

    def use(self, character) -> bool:
        character.collect_treasure(self.cost)
        return True

    def __repr__(self):
        return "*."

# Фабрика для создания предметов
class ItemFactory:
    @staticmethod
    def create_item(item_type: str, max_power: float = 2) -> Optional[Items]:
        if item_type == "food":
            return Food()
        elif item_type == "weapon":
            return Weapon(max_power)
        elif item_type == "elixir":
            return Elixir()
        elif item_type == "scroll":
            return Scroll()
        elif item_type == "treasure":
            return Treasure()
        return None

