# Класс "Узел", обозначает точку с координатами по x и y
class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        """Сравнение узлов для нормализации рёбер"""
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)