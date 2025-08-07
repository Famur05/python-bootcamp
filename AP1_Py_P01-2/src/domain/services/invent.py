from ..entities.items import *  # Импортируем классы предметов

class Inventory:
    def __init__(self, owner, max_items=9):
        self.owner = owner
        self.selected_itemtype_id = 0  # Выбранный тип предмета
        self.selected_item_id = 0
        self.items = {
            "food": [],  # Еда
            "weapon": [],  # Оружие
            "scroll": [],  # Свитки
            "elixir": []  # Эликсиры
        }
        self.max_items = max_items

    def add_item(self, item):
        done = False
        if item.type == "treasure":
            item.use(self.owner)
            done = True
        elif len(self.items[item.type]) < self.max_items:
            self.items[item.type].append(item)
            done = True
        return done

    def get_item_by_id(self, item_index):
        item = None  # Инициализируем переменную значением по умолчанию
        if self.selected_itemtype_id == 0:
            try:
                item = self.items.get("food")[item_index]
            except (IndexError, TypeError):
                pass  # Индекс вне диапазона или список пуст
        elif self.selected_itemtype_id == 1:
            try:
                item = self.items.get("weapon")[item_index]
            except (IndexError, TypeError):
                pass
        elif self.selected_itemtype_id == 2:
            try:
                item = self.items.get("scroll")[item_index]
            except (IndexError, TypeError):
                pass
        elif self.selected_itemtype_id == 3:
            try:
                item = self.items.get("elixir")[item_index]
            except (IndexError, TypeError):
                pass
        return item  # Если ничего не найдено, вернется None

    def drop_item(self, item_index):
        item = self.get_item_by_id(item_index)
        if(item):
            self.items[item.type].pop(item_index)

    def use_item(self, item_index):
        item = self.get_item_by_id(item_index)
        if(item and item.use(self.owner)):
            self.items[item.type].pop(item_index)

    def list_items(self):
        return self.items

    def __str__(self):
        result = "Инвентарь:\n"
        itemtype_id = 0
        for item_type, items in self.items.items():
            result += f"    {'[V] ' if self.selected_itemtype_id == itemtype_id else '[ ] '}{item_type.capitalize()}:\n"
            for i, item in enumerate(items):
                result += f"        {i}. {item.get_info()}\n"
            itemtype_id +=1
        result += '\n\n         1) Чтобы изменить тип предмета [стрелочки вверх/вниз].' \
                  '\n         2) Чтобы выбрать и использовать предмет [0-9].' \
                  '\n         3) Чтобы выйти нажми [i]'
        return result
