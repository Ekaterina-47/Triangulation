import numpy as np
import matplotlib.pyplot as plt
import random


# Параметры
n = 7  # количество точек


def generate_points():
    """Генерация точек на плоскости"""
    x_min, x_max = 0, 10
    y_min, y_max = 0, 10
    points = [(random.uniform(x_min, x_max), random.uniform(y_min, y_max)) for i in range(n)]
    plot_points(points)  # Отображение точек на графике
    return points


def plot_points(points):
    """График исходного набора точек"""
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    plt.figure(figsize=[6, 6])
    plt.scatter(x_coords, y_coords)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Заданные точки на плоскости, количество: {}'.format(n))
    plt.show()


def plot_segments(segments, title):
    """Отображение отрезков на графике"""
    plt.figure(figsize=[6, 6])
    for segment in segments:
        (x1, y1), (x2, y2) = segment
        plt.plot([x1, x2], [y1, y2], marker='o')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.show()



def distance(segment):
    """Вычисление евклидова расстояния между точками"""
    point1 = np.array(segment[0])
    point2 = np.array(segment[1])
    return np.sqrt(np.sum((point1 - point2) ** 2))



def make_segments(points):
    """Создание списка отрезков, отсортированных по длинам от самого малого"""
    segments_list = []    # создание списка для хранения отрезков
    for i in range(0, len(points)):
        for j in range(i+1, len(points)):
            segment = [points[i], points[j]]   # отрезок
            segments_list.append(segment)      # добавляется в список

    # Сортировка списка отрезков
    segments_list = sorted(segments_list, key=distance)

    return segments_list


def check_intersection(segment1, segment2):
    """Проверка отрезков на пересечение"""
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return False  # Отрезки параллельны или коллинеарны

    t_a = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    t_b = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

    # Проверка на пересечение отрезков внутри своих границ
    if 0 < t_a < 1 and 0 < t_b < 1:
        return True
    else:
        return False





def greedy_triangulation(points):
    """Жадная триангуляция"""

    # Шаг1: Генерация всех возможных отрезков, соединяющих пары исходных точек, они сортируются по длинам
    segments = make_segments(points)
    plot_segments(segments, "Отображение всех возможных отрезков между точками")

    # Шаг 2: Отрезки вставляются в триангуляцию, начиная с самого короткого.
    # Если происходит пересечение с уже имеющимися, отрезок отбрасывается
    triangulation_segments = []  # список для добавленных в триангуляцию отрезков
    for segment in segments:
        is_intersecting = False
        for triangulation_segment in triangulation_segments:
            if check_intersection(segment, triangulation_segment):
                is_intersecting = True
                break
        if not is_intersecting:
            triangulation_segments.append(segment)
            #plot_segments(triangulation_segments, "Добавлен отрезок")

    plot_segments(triangulation_segments, 'Работа алгоритма "Жадной триангуляции"')


# Генерация точек на плоскости
points = generate_points()

# Запуск алгоритма жадной триангуляции
greedy_triangulation(points)

