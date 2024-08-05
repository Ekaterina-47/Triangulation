
class Vector:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.x_component = end_point.x - start_point.x
        self.y_component = end_point.y - start_point.y

    def __str__(self):
        return "Вектор [начало: {}, конец: {}]".format(self.start_point, self.end_point)