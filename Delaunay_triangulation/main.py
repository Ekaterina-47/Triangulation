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
    plt.scatter(x_coords, y_coords, color='blue', s=20)
    plt.title('Заданные случайные точки')
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
            plt.scatter(x_coords, y_coords, color='blue', s=20)
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
    triangles = [super_triangle]     # начальная триангуляция (список треугольников) содержит объект супертреугольника
    plot_triangulation(triangles, "Проверка созданной суперструктуры")

    print("Супертреугольник: {}".format(super_triangle))
    print("Начальная триангуляция: {}".format(triangles))

    # Шаг 2: Поочерёдное добавление узлов в триангуляцию
    for node in nodes:
        # a) Локализация: найти, куда попадает узел
        point_localization = hitting_the_triangle(node, triangles)
        # если точка попала на ребро - вернёт список: ребро и соседние к ребру треугольники
        # если в центр треугольника - вернёт этот треугольник

        # б) Обработка узла:
        # Если узел попадает на границу треугольника (если ф-я вернула тип лист)
        if isinstance(point_localization, list):
            print("Точка попала на ребро")
            plot_triangulation(triangles, "Точка попала на ребро")
            # Распаковка списка
            now_edge = point_localization[0]     # Первым элементом является ребро, на которое попала точка
            triangle1 = point_localization[1]    # Вторым элементом стоит треугольник
            triangle2 = None                     # Второй соседний треугольник может отсутствовать, если это граница
            if len(point_localization) == 3:     # Если вернулся список с тремя элементами, то второй треугольник есть
                triangle2 = point_localization[2]

            # Нужно разделить текущие треугольники на два, получив четыре новых
            triangle_list = []  # Здесь будут сохраняться новые треугольники
            new_triangle1, new_triangle2, new_triangle3, new_triangle4 = None, None, None, None
            # Разделяю первый.
            # Определю противолежащий к точке узел треугольника, два другие известны из ребра
            opposite_point = None
            for p in triangle1.nodes:
                if p != now_edge.node1 and p != now_edge.node2:
                    opposite_point = p     # Определила противолежащий узел - не является концом ребра с точкой

                # Удаление исходного треугольника из триангуляции
                triangles.remove(triangle1)
                # Удаление этого треугольника у всех его рёбер
                for edge in triangle1.edges:
                    edge.delete_triangle(triangle1)
                plot_triangulation(triangles, "Удаление треугольника или двух")

                # Создание из него двух новых треугольников:
                new_triangle1 = Triangle(now_edge.node1, node, opposite_point)
                new_triangle2 = Triangle(now_edge.node2, node, opposite_point)
                # Добавление их в список
                triangle_list.extend([new_triangle1, new_triangle2])

            # Разделяю второй, если он есть
            if triangle2:
                for p in triangle2.nodes:
                    if p != now_edge.node1 and p != now_edge.node2:
                        opposite_point = p  # Определила противолежащий узел - не является концом ребра с точкой

                    # Удаление исходного треугольника из триангуляции
                    triangles.remove(triangle2)
                    # Удаление этого треугольника у всех его рёбер
                    for edge in triangle2.edges:
                        edge.delete_triangle(triangle2)

                    # Создание двух новых треугольников из текущего целого:
                    new_triangle3 = Triangle(now_edge.node1, node, opposite_point)
                    new_triangle4 = Triangle(now_edge.node2, node, opposite_point)
                    triangle_list.extend([new_triangle3, new_triangle4])

            # Установка соседей для новых треугольников (можно их посмотреть по рёбрам)
            for new_triangle in triangle_list:
                for edge in new_triangle.edges:
                    for triangle_neighbour in edge.triangles:
                        if triangle_neighbour != new_triangle:
                            new_triangle.add_neighbour(triangle_neighbour)

            triangles.extend(triangle_list)
 #           plot_triangulation(triangles, "Вставка новых треугольников")


            # Проверка условия Делоне для каждого нового треугольника и точки соседнего треугольника
            for triangle in triangle_list:
                for neighbour in triangle.neighboring_triangles:
                    for point in neighbour.nodes:
                        if point not in triangle.nodes:
                            if delaunay_condition(triangle.nodes[0], triangle.nodes[1], triangle.nodes[2], point):
                                continue
                            else:
                                # Если условие не выполняется, производится флип ребра,
                                # треугольники заменяются новыми
                                flip_edge(triangles, triangle, neighbour, point)
                                break
                    break
#            plot_triangulation(triangles, "Результат после проверки")




            # После проверки условия Делоне и преобразований новые треугольники вставляются в триангуляцию
            triangles.extend([new_triangle1, new_triangle2])
            if new_triangle3 and new_triangle4:
                triangles.extend([new_triangle3, new_triangle4])


        # Если узел попадает внутрь треугольника
        if isinstance(point_localization, Triangle):
#            print("Точка попала внутрь треугольника")
            triangle = point_localization
 #           plot_triangulation(triangles, "Точка попала внутрь треугольника")

            # Надо сразу удалить этот треугольник из триангуляции и освободить рёбра от связи с ним
            # Удаление старого треугольника
            triangles.remove(triangle)
 #           plot_triangulation(triangles, "Удалён старый треугольник, который разделён на 3")
            # Удаление этого треугольника у всех его рёбер
            for edge in triangle.edges:
                edge.delete_triangle(triangle)

            # Разделение треугольника на три новых
            new_triangle1 = Triangle(triangle.nodes[0], triangle.nodes[1], node)
            new_triangle2 = Triangle(triangle.nodes[1], triangle.nodes[2], node)
            new_triangle3 = Triangle(triangle.nodes[2], triangle.nodes[0], node)

            # Установка соседей для новых треугольников (можно их посмотреть по рёбрам)
            for new_triangle in [new_triangle1, new_triangle2, new_triangle3]:
                for edge in new_triangle.edges:
                    for triangle_neighbour in edge.triangles:
                        if triangle_neighbour != new_triangle and len(new_triangle.neighboring_triangles) < 3:
                            new_triangle.add_neighbour(triangle_neighbour)

            # Вставка новых треугольников в триангуляцию
            triangles.extend([new_triangle1, new_triangle2, new_triangle3])
 #           plot_triangulation(triangles, "Установка трёх новых треугольников")

            # Проверка условия Делоне для каждого нового треугольника и точки соседнего треугольника
            for triangle in [new_triangle1, new_triangle2, new_triangle3]:
                for neighbour in triangle.neighboring_triangles:
                    for point in neighbour.nodes:
                        if point not in triangle.nodes:
                            if delaunay_condition(triangle.nodes[0], triangle.nodes[1], triangle.nodes[2], point):
                                continue
                            else:
                                # Если условие не выполняется, производится флип ребра,
                                # треугольники заменяются новыми
                                flip_edge(triangles, triangle, neighbour, point)
                                break
                    break
 #           plot_triangulation(triangles, "Результат после проверки")

    plot_triangulation(triangles, "Итоговая триангуляция с суперструктурой")
    # Шаг 3: Удалить треугольники, которые содержат узлы супертреугольника, чтобы они не оказались в финальной триангуляции
    total_triangles = [triangle for triangle in triangles if not any(node in super_triangle.nodes for node in triangle.nodes)]

    # Дополнительная коррекция итоговой триангуляции
    correct = 1
    while (correct != 0):
        correct = 1
        for triangle in triangles:
            for neighbour in triangle.neighboring_triangles:
                for point in neighbour.nodes:
                    if point not in triangle.nodes:
                        if delaunay_condition(triangle.nodes[0], triangle.nodes[1], triangle.nodes[2], point):
                            continue
                        else:
                            correct += 1
                            print("Не выполняется условие Делоне")
                            flip_edge(triangles, triangle, neighbour, point)
                            break
                break
        correct -= 1


    # Шаг 4: Вернуть список треугольников, представляющих финальную триангуляцию
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
num_points = 100
x_range = (-10, 10)
y_range = (-10, 10)
random_points = generate_random_points(num_points, x_range, y_range)

plot_initial_points(random_points)
print(random_points)


triangles = delaunay_triangulation(random_points)

print("Количество итоговых треугольников: {}".format(len(triangles)))
# print("\n Треугольники в финальной триангуляции:\n{}".format(triangles))
plot_triangulation(triangles, "Финальная триангуляция")


