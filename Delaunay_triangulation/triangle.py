from node import Node
from edge import Edge

# Класс "Треугольник", хранит в качестве свойств три узла, рёбра и ссылки на соседние треугольники
class Triangle:

    def __init__(self, node1, node2, node3):

        self.nodes = [node1, node2, node3]                # Список точек треугольника

        self.edges = [self.create_edge(node1, node2),
                      self.create_edge(node2, node3),
                      self.create_edge(node3, node1)]     # Список рёбер треугольника

        self.neighboring_triangles = [None, None, None]   # Ссылки на соседние треугольники, если есть

    # Создание ребра по переданным точкам
    def create_edge(self, node1, node2):
        edge = Edge(node1, node2)
        edge.add_triangle(self)
        return edge

    def set_neighbor(self, edge, neighbor):
        for i, e in enumerate(self.edges):
            if (e.node1 == edge.node1 and e.node2 == edge.node2) or \
                    (e.node1 == edge.node2 and e.node2 == edge.node1):
                self.neighboring_triangles[i] = neighbor
                return


    # Получение соседнего треугольника для данного ребра
    def get_neighbor(self, edge):
        for i, e in enumerate(self.edges):
            if (e.node1 == edge.node1 and e.node2 == edge.node2) or \
               (e.node1 == edge.node2 and e.node2 == edge.node1):
                return self.neighboring_triangles[i]
        return None

    # Определение узлов, противоположных ребру
    def find_opposite_nodes(self, edge):
        nodes = [node for node in self.nodes if node not in [edge.node1, edge.node2]]
        if len(nodes) == 1:
            return nodes[0]
        return None


    def __repr__(self):
        return (f"Треугольник.\n (точки: {self.nodes}, ")
                #f"\nрёбра: {self.edges},"
                #f"\n соседние треугольники: {self.neighboring_triangles})")

