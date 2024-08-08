import math

import numpy as np

from node import Node
from triangle import Triangle
from vector import Vector
from edge import Edge
# Вспомогательные функции

# Функция для создания суперструктуры в форме треугольника
def create_super_triangle(nodes, magnification_factor=4):
    """Вычисляются границы (минимальные и максимальные координаты) всех узлов
    и создаётся супер-треугольник, включающий в себя все узлы"""

    # Нахождение границ на плоскости по OX и OY, определяющую область, в которой расположены узлы
    min_x = min(node.x for node in nodes)
    max_x = max(node.x for node in nodes)
    min_y = min(node.y for node in nodes)
    max_y = max(node.y for node in nodes)

    # Вычисление радиуса и центра у найденной области, он увеличивается на коэффициент
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    radius = max(max_x - min_x, max_y - min_y) / 2 * magnification_factor

    # вычиcление вершин равностороннего треугольника, которые лежат на окружности
    angles = [0, 2 * math.pi / 3, 4 * math.pi / 3]
    vertices = [
        Node(
            center_x + radius * math.cos(angle),
            center_y + radius * math.sin(angle)
        )
        for angle in angles
    ]

    super_triangle_object = Triangle(vertices[0], vertices[1], vertices[2])
    return super_triangle_object


# Функция для псевдоскалярного произведения
def vector_cross_product(vector_1, vector_2):
    return vector_1.x_component * vector_2.y_component - vector_1.y_component * vector_2.x_component

# Функция для локализации точки
def hitting_the_triangle(point, triangles):

    location_list = []    # Если точка попадёт на ребро, то здесь будёт это ребро и два треугольника, которому оно принадлежит

    # Проверяю все треугольники из текущей триангуляции, попала ли туда точка
    for triangle in triangles:

        # Получение координат треугольника
        vertex_1 = triangle.nodes[0]
        vertex_2 = triangle.nodes[1]
        vertex_3 = triangle.nodes[2]

        # Построение трёх векторов
        vector_1 = Vector(vertex_1, point)
        vector_2 = Vector(vertex_2, point)
        vector_3 = Vector(vertex_3, point)

        # Вычисление псевдоскалярных произведений
        product_1 = vector_cross_product(vector_1, Vector(vertex_1, vertex_2))
        product_2 = vector_cross_product(vector_2, Vector(vertex_2, vertex_3))
        product_3 = vector_cross_product(vector_3, Vector(vertex_3, vertex_1))

        # Проверка, не равно ли какое-то из произведений нулю.
        # Тогда будет так, что точка попала на границу ребра треугольника, то сохраняется в список это ребро и треугольник
        if product_1 == 0:
            if len(location_list) == 0:
                location_list.append(Edge(vertex_1, vertex_2))
                location_list.append(triangle)
            else:
                location_list.append(triangle)
        if product_2 == 0:
            if len(location_list) == 0:
                location_list.append(Edge(vertex_2, vertex_3))
                location_list.append(triangle)
            else:
                location_list.append(triangle)

        if product_3 == 0:
            if len(location_list) == 0:
                location_list.append(Edge(vertex_3, vertex_1))
                location_list.append(triangle)
            else:
                location_list.append(triangle)


        # Если знаки у векторных произведений совпадут - это озн., что точка внутри треугольника. Вернётся этот треугольник
        if (product_1 > 0 and product_2 > 0 and product_3 > 0) or (product_1 < 0 and product_2 < 0 and product_3 < 0):
            return triangle

    # Вернётся список с ребром и двумя треугольниками
    return location_list




def delaunay_condition(node1, node2, node3, point):
    """Проверка выполнения условия Делоне через уравнение описанной окружности"""

    # Координаты точек треугольника
    x1, y1 = node1.x, node1.y
    x2, y2 = node2.x, node2.y
    x3, y3 = node3.x, node3.y
    x0, y0 = point.x, point.y

    # Пояснение.
    # Уравнение окружности, проходящей через точки (x1, y1), (x2, y2), (x3, y3), можно записать в виде:
    # matrix = np.array([
    #     [x1 ** 2 + y1 ** 2, x1, y1, 1],
    #     [x2 ** 2 + y2 ** 2, x2, y2, 1],
    #     [x3 ** 2 + y3 ** 2, x3, y3, 1],
    #     [x0 ** 2 + y0 ** 2, x0, y0, 1],
    # ])


   # Матрицы для вычисления определителей:
    a = np.array([
        [x1, y1, 1],
        [x2, y2, 1],
        [x3, y3, 1]
    ])

    b = np.array([
        [x1 ** 2 + y1 ** 2, y1, 1],
        [x2 ** 2 + y2 ** 2, y2, 1],
        [x3 ** 2 + y3 ** 2, y3, 1],
    ])

    c = np.array([
        [x1 ** 2 + y1 ** 2, x1, 1],
        [x2 ** 2 + y2 ** 2, x2, 1],
        [x3 ** 2 + y3 ** 2, x3, 1],
    ])

    d = np.array([
        [x1 ** 2 + y1 ** 2, x1, y1],
        [x2 ** 2 + y2 ** 2, x2, y2],
        [x3 ** 2 + y3 ** 2, x3, y3],
    ])

    # Условие Делоне для любого заданного треугольника будет выполняться только тогда,
    # когда для любого узла триангуляции (x0, y0)
    # будет (det_a * (x0 ** 2 + y0 ** 2) - det_b * x0 + det_c * y0 - det_d) * np.sign(det_a) >= 0,
    # т.е. когда (x0, y0) не попадает внутрь окружности, описанной вокруг треугольника

    # вычисление определителей
    det_a = np.linalg.det(a)
    det_b = np.linalg.det(b)
    det_c = np.linalg.det(c)
    det_d = np.linalg.det(d)

    # True - выполняется, False - не выполняется
    return (det_a * (x0 ** 2 + y0 ** 2) - det_b * x0 + det_c * y0 - det_d) * np.sign(det_a) >= 0

# Функция для флипа ребра
def flip_edge(triangle, neighbour_triangle):
    """
    Если условие Делоне не выполняется, то необходимо осуществить флип ребра.
    В качестве параметров функция принимает треугольник, окружность которого исследуется,
    и его соседний треугольник, точка которого попала в окружность.
    Формируются два новых треугольника таким образом:
        Исходные треугольники:                     После флипа:
                C                                      С
               / \                                    /|\
              /   \                                  / | \
             /     \                                /  |  \
           A ------- B                            A    |    B
                                                   \   |   /
                                                    \  |  /
                                                     \ | /
                                                      \|/
                D                                      D
    """

    # Определение общего ребра треугольника и переданного соседа
    common_edge = None
    for e1 in triangle.edges:
        for e2 in neighbour_triangle.edges:
            if (e1.node1 == e2.node1 and e1.node2 == e2.node2) or (e1.node1 == e2.node2 and e1.node2 == e2.node1):
                common_edge = e1
                break
        if common_edge:
            break

    # Если общего ребра нет - исключение
    if not common_edge:
        raise ValueError("Нет общего ребра у переданных треугольников.")

    A, B = common_edge.node1, common_edge.node2

    C = next(p for p in triangle.nodes if p != A and p != B)
    D = next(p for p in neighbour_triangle.nodes if p != A and p != B)

    # Создание новы[ треугольников
    converted_triangle1 = Triangle(A, C, D)
    converted_triangle2 = Triangle(B, C, D)

    # Установка соседей для новых треугольников
    converted_triangle1.set_neighbor(Edge(A, C), triangle.get_neighbor(Edge(A, C)))
    converted_triangle1.set_neighbor(Edge(C, D), converted_triangle2)
    converted_triangle1.set_neighbor(Edge(D, A), neighbour_triangle.get_neighbor(Edge(D, A)))

    converted_triangle2.set_neighbor(Edge(B, C), triangle.get_neighbor(Edge(B, C)))
    converted_triangle2.set_neighbor(Edge(C, D), converted_triangle1)
    converted_triangle2.set_neighbor(Edge(D, B), neighbour_triangle.get_neighbor(Edge(D, B)))

    return converted_triangle1, converted_triangle2