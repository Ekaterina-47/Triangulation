# Класс "Узел", обозначает точку с координатами по x и y
class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Узел ({}, {})".format(self.x, self.y)