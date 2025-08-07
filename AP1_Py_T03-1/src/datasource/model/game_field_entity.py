class GameFieldEntity:
    def __init__(self, matrix=None):
        self.matrix = matrix if matrix else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]