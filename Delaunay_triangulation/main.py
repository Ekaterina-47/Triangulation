import numpy as np
import matplotlib.pyplot as plt
import random

from node import Node
from edge import Edge
from triangle import Triangle
from ulits import create_super_triangle, delaunay_condition, hitting_the_triangle, flip_edge


def plot_initial_points(nodes):
    """
    Функция для построения графика с исходными точками.
    """
    x_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]

    plt.figure(figsize=(10, 10))
    plt.scatter(x_coords, y_coords, color='blue')
    plt.title('Initial Points')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def plot_triangulation(triangles, title=''):
    """
    Функция для построения графика с рёбрами итоговой триангуляции.
    """
    plt.figure(figsize=(10, 10))

    for triangle in triangles:
        for edge in triangle.edges:
            x_coords = [edge.node1.x, edge.node2.x]
            y_coords = [edge.node1.y, edge.node2.y]
            plt.plot(x_coords, y_coords, color='black')

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def delaunay_triangulation(nodes):
    # Проверка, что узла не меньше, чем 3
    if len(nodes) < 3:
        return "Количество узлов: {}, триангуляция не нужна.".format(len(nodes))

    # Если узла три, то триангуляцией будет один треугольник
    if len(nodes) == 3:

        return [Triangle(nodes[0], nodes[1], nodes[2])]

    # Основные шаги алгоритма

    # Шаг 1: Инициализация. Создание начальной триангуляции с помощью треугольника, охватывающего все точки
    super_triangle = create_super_triangle(nodes)
    triangles = [super_triangle]     # начальный список треугольников содержит объект супертреугольника
    plot_triangulation(triangles, "Проверка созданной суперструктуры")

    print("Супертреугольник: {}".format(super_triangle))
    print("Начальная триангуляция: {}".format(triangles))

    # Шаг 2: Поочерёдное добавление узлов в триангуляцию
    for node in nodes:
        # a) Локализация: найти треугольник, в который попадает данный узел, или ближайший треугольник на границе триангуляции

        point_localization = hitting_the_triangle(node, triangles)    # FIXME Исправить локализацию: определить треугольник и ребро
        # если попала на ребро - вернёт ребро
        # если в центр треугольника - вернёт этот треугольник

        # б) Обработка узла:
        # Если узел попадает на границу треугольника (если ф-я вернула тип лист)
        if isinstance(point_localization, list):

            print("Точка попала на ребро")
            plot_triangulation(triangles, "Точка попала на ребро")


            now_edge = point_localization[0]
            triangle1 = point_localization[1]
            if len(plot_triangulation) == 3:
                triangle2 = point_localization[2]


            # Нужно разделить текущие треугольники на два.
            # Разделяю первый.
            # Определю противолежащий к точке узел треугольника, два другие известны из ребра
            for p in triangle1.nodes:
                if p != now_edge.node1 and p != now_edge.node2:
                    opposite_point = p     # Определила противолежащий узел - не является концом ребра с точкой

                # Создание двух новых треугольников из текущего целого:
                new_triangle1 = Triangle(now_edge.node1, node, opposite_point)
                new_triangle2 = Triangle(now_edge.node2, node, opposite_point)
            # Разделяю второй
            if len(plot_triangulation) == 3:

                for p in triangle2.nodes:
                    if p != now_edge.node1 and p != now_edge.node2:
                        opposite_point = p  # Определила противолежащий узел - не является концом ребра с точкой

                    # Создание двух новых треугольников из текущего целого:
                    new_triangle3 = Triangle(now_edge.node1, node, opposite_point)
                    new_triangle4 = Triangle(now_edge.node2, node, opposite_point)


            if len(plot_triangulation) == 2:
                triangle_list = [new_triangle1, new_triangle2]
            if len(plot_triangulation) == 3:
                triangle_list = [new_triangle1, new_triangle2, new_triangle3, new_triangle4]
            for new_triangle in triangle_list:
                # Установка соседних треугольников для новых
                for other_triangle in triangles:
                    if other_triangle != new_triangle:
                        for e1 in new_triangle.edges:
                            for e2 in other_triangle.edges:
                                if (e1.node1 == e2.node1 and e1.node2 == e2.node2) or (
                                        e1.node2 == e2.node1 and e1.node1 == e2.node2):
                                    for i in range(len(new_triangle.neighboring_triangles)):
                                        if new_triangle.neighboring_triangles[i] is None:
                                            new_triangle.neighboring_triangles[i] = other_triangle
                                            break



                # Проверка выполнения условия Делоне
#                for new_triangle in triangle_list:
#                    for neighbour in new_triangle.neighboring_triangles:
#                        if neighbour:
#                            for point in range(len(neighbour.nodes)):
#                                if delaunay_condition(new_triangle.nodes[0], new_triangle.nodes[1], new_triangle.nodes[2], neighbour.nodes[point]):
#                                    print("Выполняется")
#                                    continue
#                                else:
#                                    new_triangle, neighbour = flip_edge(new_triangle, neighbour)
#                                    print("флип")
#                                    break


                triangles.remove(triangle1)
                if len(point_localization) == 3:
                    triangles.remove(triangle2)
                plot_triangulation(triangles, "Удалёны старые треугольники")
                for triangle in triangle_list:
                    triangles.append(triangle)
                plot_triangulation(triangles, "Добавлено четыре треугольника")

            #    triangles.append(new_triangle2)


                # Если узел попадает внутрь треугольника
        if isinstance(point_localization, Triangle):
            print("Точка попала внутрь треугольника")
            triangle = point_localization

            plot_triangulation(triangles, "Точка попала внутрь треугольника")

            # Разделение треугольника на три новых
            new_triangle1 = Triangle(triangle.nodes[0], triangle.nodes[1], node)
            new_triangle2 = Triangle(triangle.nodes[1], triangle.nodes[2], node)
            new_triangle3 = Triangle(triangle.nodes[2], triangle.nodes[0], node)

            # Установка соседних треугольников между новыми треугольниками
            new_triangle1.neighboring_triangles = [new_triangle2, new_triangle3, None]
            new_triangle2.neighboring_triangles = [new_triangle3, new_triangle1, None]
            new_triangle3.neighboring_triangles = [new_triangle1, new_triangle2, None]

            # Удаление старого треугольника
            triangles.remove(triangle)
            plot_triangulation(triangles, "Удалён старый треугольник, который разделён на 3")


                # Проверка выполнения условия Делоне
            for new_triangle in [new_triangle1, new_triangle2, new_triangle3]:
                if len(triangles) == 0:
                    break
                for neighbour in new_triangle.neighboring_triangles:
                    if neighbour:
                        for point in range(len(neighbour.nodes)):
                            if delaunay_condition(new_triangle.nodes[0], new_triangle.nodes[1], new_triangle.nodes[2], neighbour.nodes[point]):
                                plot_triangulation(triangles, "Делоне выполняется")
                                print("Выполняется")
                            else:
                                new_triangle, neighbour = flip_edge(new_triangle, neighbour)
                                plot_triangulation(triangles, "Делоне не выполняется, производится флип")
                                print("Флип")
                                continue

            triangles.extend([new_triangle1, new_triangle2, new_triangle3])
            plot_triangulation(triangles, "Установнено три новых треугольника")

            #break
    plot_triangulation(triangles, "Итоговая триангуляция с суперструктурой")
    # Шаг 3: Удалить треугольники, которые содержат узлы супертреугольника, чтобы они не оказались в финальной триангуляции
    total_triangles = [triangle for triangle in triangles if not any(node in super_triangle.nodes for node in triangle.nodes)]

    # Шаг 4: Вернуть список треугольников, представляющих финальную триангуляцию

    print(len(total_triangles))
    return total_triangles


# Использование алгоритма
def generate_random_points(num_points, x_range, y_range):

    points = []
    for _ in range(num_points):
        x = random.uniform(x_range[0], x_range[1])
        y = random.uniform(y_range[0], y_range[1])
        points.append(Node(x, y))
    return points

# Тестирование
num_points = 4
x_range = (-10, 10)
y_range = (-10, 10)
random_points = generate_random_points(num_points, x_range, y_range)

plot_initial_points(random_points)
print(random_points)


triangles = delaunay_triangulation(random_points)

print("Количество итоговых треугольников: {}".format(num))
print("\n Треугольники в финальной триангуляции:\n{}".format(triangles))
plot_triangulation(triangles, "Финальная триангуляция")

