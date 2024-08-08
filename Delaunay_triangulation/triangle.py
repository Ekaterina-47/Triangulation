from node import Node
from edge import Edge

# Класс "Треугольник", хранит в качестве свойств три узла, рёбра и ссылки на соседние треугольники
class Triangle:

    edges_list = []  # Здесь будет информация о всех созданных рёбрах у треугольников
                # Может быть это будет не список.
                # Нужно будет сделать так, чтобы при создании ребра, проверялось,
    # вдруг оно уже тут есть, тогда просто тут ему добавляется соседний треугольник.
    # А если его тут нет, то оно будет создаваться, будет добавляться треугольник-сосед (автоматически) и сюда записываться
    # Нужно будет придумать оптимальную структуру, как это будет храниться.

    def __init__(self, node1, node2, node3):

        self.nodes = [node1, node2, node3]                # Список точек треугольника

        self.edges = [self.create_edge(node1, node2),
                      self.create_edge(node2, node3),
                      self.create_edge(node3, node1)]     # Список рёбер треугольника

        self.neighboring_triangles = []   # Ссылки на соседние треугольники, если есть

    # Создание ребра по переданным точкам
    def create_edge(self, node1, node2):
        # Создалось ребро по переданным точкам
        new_edge = Edge(node1, node2)

        # Проверка, не равно ли это ребро какому-то из уже созданных

        if len(Triangle.edges_list) > 1:
            for edge in Triangle.edges_list:
                # Если такое ребро уже есть, то использую его здесь, добавляю ему этот треугольник как соседа
                if new_edge == edge:
                    edge.add_triangle(self)
                    return edge
        # Иначе я использую новое созданное, ему присваиваю этот треугольник и добавляю в список всех рёбер
        new_edge.add_triangle(self)
        Triangle.edges_list.append(new_edge)
        return new_edge


    # Добавление соседних треугольников
    def add_neighbour(self, *triangles):
        if len(triangles) < 1 or len(triangles) > 3:
            raise ValueError("Функция должна принимать от 1 до 3 треугольников")
        for triangle in triangles:
            if len(self.neighboring_triangles) < 3:
                self.neighboring_triangles.append(triangle)
            else:
                raise ValueError("Нельзя добавить больше трёх соседей для треугольника")


    def __repr__(self):
        return (f"Треугольник.\n Точки: ({self.nodes},\n"
                f"Рёбра: \n{self.edges},")
#                f"\n соседние треугольники: {self.neighboring_triangles})")

