#pragma once
#include "Point.h"

using namespace std;


// Объявление класса для отрезков
class Segment {

private:
	Point start;
	Point end;

	double segmentLength;

public:

	// Конструктор для отрезка
	Segment(const Point& start, const Point& end);

	// Методы

	Point getStart() const;      // Получить начальную точку
	Point getEnd() const;        // Получить конечную точку

	double getLength() const;                        // Вычисление длинны отрезка
	bool intersection(const Segment& other) const;   // Проверка на пересечение с другим отрезком
};