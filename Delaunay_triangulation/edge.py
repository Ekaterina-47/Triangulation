from node import Node

# Класс "Рёбро", хранит в качестве свойств два узла и ссылки на треугольники, которые делят это ребро
class Edge:

    def __init__(self, node1, node2):

        # Ребро создаётся с фиксированным порядком точек
        self.node1 = min(node1, node2)
        self.node2 = max(node1, node2)
        self.triangles = []  # Информация о треугольниках, которым принадлежит ребро

    # Добавление треугольника, которому принадлежит ребро (при создании треугольника, он автоматически запишется)
    def add_triangle(self, triangle):
        if len(self.triangles) < 2:
            self.triangles.append(triangle)

    def delete_triangle(self, triangle):
        if triangle in self.triangles:
            self.triangles.remove(triangle)

    # Для сравнения с помощью "==" рёбер у разных треугольников. Рёбра могут быть сохранены в разных участках памяти
    def __eq__(self, other):
        if self.node1 == other.node1 and self.node2 == other.node2:
            return True
        else:
            return False

    # Для этих же целей, если понадобится "!="
    def __ne__(self, other):
        if self.node1 != other.node1 or self.node2 != other.node2:
            return True
        else:
            return False

    def __repr__(self):
        return (f"|{self.node1},{self.node2}|")
