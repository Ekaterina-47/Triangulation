from node import Node

# Класс "Рёбро", хранит в качестве свойств два узла и ссылки на треугольники, которые делят это ребро
class Edge:

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.triangles = [None, None]  # Ребро хранит информацию о двух треугольниках, если они есть

    def add_triangle(self, triangle):
        if self.triangles[0] is None:
            self.triangles[0] = triangle
        elif self.triangles[1] is None:
            self.triangles[1] = triangle
        else:
            raise ValueError("Ребро не может быть связано более чем с двумя треугольниками.")

    def remove_triangle(self, triangle):
        if self.triangles[0] == triangle:
            self.triangles[0] = None
        elif self.triangles[1] == triangle:
            self.triangles[1] = None

    def __repr__(self):
        return (f"Ребро ({self.node1},{self.node2}")
                #f","
              #  f"\nСвязанные треугольники: {self.triangles})")
