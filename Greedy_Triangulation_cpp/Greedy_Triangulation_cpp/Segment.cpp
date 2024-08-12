#include "Segment.h"
#include <cmath>

using namespace std;

// Реализация конструктора и методов для класса Segment


// Конструктор
Segment::Segment(const Point& start, const Point& end) : start(start), end(end) {}



// Получить начало отрезка
Point Segment::getStart() const{
	return start;
}

// Получить конец отрезка
Point Segment::getEnd() const {
	return end;
}

// Вычисление длинны отрезка
double Segment::getLength() const {
	return start.distance(end);
}


// Проверка на пересечение с другим отрезком
	bool Segment::intersection(const Segment & other) const {
		double x1 = start.getX(), y1 = start.getY();
		double x2 = end.getX(), y2 = end.getY();
		double x3 = other.getStart().getX(), y3 = other.getStart().getY();
		double x4 = other.getEnd().getX(), y4 = other.getEnd().getY();

		double denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);

		if (denominator == 0) {
			return false;        // Отрезки параллельны или коллинеарны
		}

		double t_a = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator;
		double t_b = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator;

		// Проверка на пересечение отрезков внутри своих границ
		if (0 < t_a && t_a < 1 && 0 < t_b && t_b < 1) {
			return true;
		}
		else
		{
			return false;
		}
	}