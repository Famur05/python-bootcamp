class GameField:
    def __init__(self, matrix=None):
        '''0 - пустая клетка, 1 - пользователь, 2 - компьютер'''
        self.matrix = matrix if matrix else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    def get_matrix(self):
        return self.matrix
    
    def set_matrix(self, matrix):
        self.matrix = matrix