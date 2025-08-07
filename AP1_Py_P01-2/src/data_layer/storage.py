import json
import pickle
import base64


def obj_to_json(obj):
    pickled = pickle.dumps(obj)
    coded = base64.b64encode(pickled).decode('utf8')
    return json.dumps(coded)

def json_to_obj(s):
    coded = base64.b64decode(s)
    return pickle.loads(coded)

def save_progress(game_model):
    try:
        with open("Save.json", 'w') as f:
            obj = obj_to_json(game_model)
            json.dump(obj, f, indent=4)
    except Exception as e:
        pass

def load_progress():
    result = None
    try:
        with open("Save.json", 'r') as f:
            j = json.load(f)
            GameModel = json_to_obj(j)
            if(GameModel.running == True):
                result = GameModel
    except:
        pass
    return result










# import json
# import os
#
# class DataLayer:
#     def __init__(self, filename="savegame.json"):
#         self.filename = filename
#         self.data = {
#             "current_progress": {},
#             "history": []
#         }
#         self.load_data()
#
#     def load_data(self):
#         if os.path.exists(self.filename):
#             with open(self.filename, "r") as file:
#                 self.data = json.load(file)
#
#     def save_current_progress(self, level, stats):
#         self.data["current_progress"] = {
#             "level": level,
#             "stats": stats
#         }
#         self._save_to_file()
#
#     def save_attempt(self):
#         if self.data["current_progress"]:
#             self.data["history"].append(self.data["current_progress"])
#             self.data["history"].sort(key=lambda x: x["stats"].get("treasures", 0), reverse=True)  # Сортировка по сокровищам
#             self.data["current_progress"] = {}
#             self._save_to_file()
#
#     def get_current_progress(self):
#         return self.data.get("current_progress", {})
#
#     def get_statistics(self):
#         """Возвращает всю статистику прохождений"""
#         return self.data.get("history", [])
#
#     def _save_to_file(self):
#         """Сохраняет данные в JSON-файл"""
#         with open(self.filename, "w") as file:
#             json.dump(self.data, file, indent=4)
#
# data_layer = DataLayer()
#
# data_layer.save_current_progress(level=3, stats={
#     "treasures": 12,    # Количество сокровищ
#     "enemies_defeated": 5,  # Побежденные враги
#     "food_eaten": 3,     # Съеденная еда
#     "potions_used": 2,   # Выпитые эликсиры
#     "scrolls_read": 1,   # Прочитанные свитки
#     "damage_dealt": 45,  # Нанесенный урон
#     "damage_taken": 20,  # Полученный урон
#     "cells_traveled": 150  # Пройденные клетки
# })
#
# progress = data_layer.get_current_progress()
# print("Текущий прогресс:", progress)
#
# data_layer.save_attempt()
#
# history = data_layer.get_statistics()
# print("Статистика всех попыток:", history)
