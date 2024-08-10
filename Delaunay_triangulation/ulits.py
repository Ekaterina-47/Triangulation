import math

import numpy as np

from node import Node
from triangle import Triangle
from vector import Vector
from edge import Edge
# Вспомогательные функции

# Функция для создания суперструктуры в форме треугольника
def create_super_triangle(nodes, magnification_factor=3):
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

    location_list = []    # Если точка попадёт на ребро, то здесь будёт храниться
    # это ребро и два треугольника, которому оно принадлежит

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
        # Тогда будет так, что точка попала на границу ребра треугольника.
        # Сохраняется это ребро и его соседние к нему треугольники
        if product_1 == 0:
            now_edge = Edge(vertex_1, vertex_2)
            for edge in Triangle.edges_list:
                # Если такое ребро уже есть (а оно должно быть), то использую его
                if now_edge == edge:
                    location_list.append(edge)
                    for triangle_n in edge.triangles:
                        location_list.append(triangle_n)
                    break
                # Если ребро не нашлось в списке, то что-то пошло не так
                else:
                    raise ValueError("Ошибка в функции локализации, не определено ребро")

        # Аналогичная проверка для второго
        if product_2 == 0:
            now_edge = Edge(vertex_2, vertex_3)
            for edge in Triangle.edges_list:
                if now_edge == edge:
                    location_list.append(edge)
                    for triangle_n in edge.triangles:
                        location_list.append(triangle_n)
                    break
                else:
                    raise ValueError("Ошибка в функции локализации, не определено ребро")

        # И для третьего псевдоскалярного произведения
        if product_3 == 0:
            now_edge = Edge(vertex_3, vertex_1)
            for edge in Triangle.edges_list:
                if now_edge == edge:
                    location_list.append(edge)
                    for triangle_n in edge.triangles:
                        location_list.append(triangle_n)
                    break
                else:
                    raise ValueError("Ошибка в функции локализации, не определено ребро")

        # Если знаки у векторных произведений совпадут - это означает, что точка внутри треугольника.
        if (product_1 > 0 and product_2 > 0 and product_3 > 0) or (product_1 < 0 and product_2 < 0 and product_3 < 0):
            # Вернётся этот треугольник
            return triangle

    # Если точка попала на ребро, вернётся список с ребром и двумя треугольниками
    return location_list


def delaunay_condition(node1, node2, node3, point):
    """
    Проверка выполнения условия Делоне через уравнение описанной окружности.
    Точка соседнего треугольника, не принадлежащая рассматриваемому, не должна попадать в окружность.
    На вход поступает три точки треугольника и одна от соседнего.
    """

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

    # Вычисление определителей
    det_a = np.linalg.det(a)
    det_b = np.linalg.det(b)
    det_c = np.linalg.det(c)
    det_d = np.linalg.det(d)

    # True - выполняется, False - не выполняется
    return (det_a * (x0 ** 2 + y0 ** 2) - det_b * x0 + det_c * y0 - det_d) * np.sign(det_a) >= 0


# Функция для флипа ребра
def flip_edge(triangles, triangle, neighbour_triangle, point):
    """
    Если условие Делоне не выполняется, то необходимо осуществить флип ребра.
    В качестве параметров функция принимает список со всеми треугольниками в триангуляции,
    треугольник, окружность которого исследуется,
    соседний треугольник, и точка, которая попала в окружность.
    Формируются два новых треугольника таким образом:
        Исходные треугольники:                     После флипа:
                C                                      С
               / \                                    /|\
              /   \                                  / | \
             /     \                                /  |  \
           A ------- B                            A    |   \ B
            \       /                              \   |   /
             \     /                                \  |  /
              \   /                                  \ | /
               \ /                                    \|/
                D                                      D
    """

    # Определение общего ребра треугольника и переданного соседа
    common_edge = None
    for edge in triangle.edges:
        for triangle_neighbour in edge.triangles:
            if triangle_neighbour == neighbour_triangle:
                common_edge = edge
                break
        break

    # Если по каким-то причинам нет общего ребра у переданных треугольников (а оно должно быть),
    # То оно пересоздаётся
    if common_edge is None:
        points = []
        for p1 in triangle.nodes:
            for p2 in neighbour_triangle.nodes:
                if p1 == p2 and len(points) < 2:
                    points.append(p1)
        common_edge = Edge(points[0], points[1])
        if common_edge in Triangle.edges_list:
            common_edge.triangles.clear()
        else:
            Triangle.edges_list.append(common_edge)
        common_edge.add_triangle(triangle)
        common_edge.add_triangle(neighbour_triangle)

    a, b = common_edge.node1, common_edge.node2

    c = next(p for p in triangle.nodes if p != a and p != b)
    d = point

    # Освобождение рёбер от связи со старыми треугольниками
    for edge in triangle.edges:
        edge.delete_triangle(triangle)
    for edge in neighbour_triangle.edges:
        edge.delete_triangle(neighbour_triangle)

    # Удаление старых треугольников из триангуляции
    triangles.remove(triangle)
    if neighbour_triangle in triangles:
        triangles.remove(neighbour_triangle)

    # Создание новых треугольников
    converted_triangle1 = Triangle(a, c, d)
    converted_triangle2 = Triangle(b, c, d)

    # Установка соседей для новых треугольников
    for new_triangle in [converted_triangle1, converted_triangle2]:
        for edge in new_triangle.edges:
            for triangle_neighbour in edge.triangles:
                if (triangle_neighbour != new_triangle and triangle_neighbour not in new_triangle.neighboring_triangles
                        and len(new_triangle.neighboring_triangles) < 3):
                    new_triangle.add_neighbour(triangle_neighbour)

    # Вставка новых треугольников в триангуляцию
    triangles.extend([converted_triangle1, converted_triangle2])
