class GameFieldDto:
    def __init__(self, matrix=None):
        self.matrix = matrix if matrix else [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    
    def to_dict(self):
        return {"matrix": self.matrix}
    
    @staticmethod
    def from_dict(data):
        if not data or "matrix" not in data:
            return GameFieldDto()
        return GameFieldDto(data["matrix"])