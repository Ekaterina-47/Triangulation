#pragma once

// Объявление класса для точек

class Point {

private:

	double x;    // Координата по X
	double y;    // Координата по Y

public:
     
	// Конструктор для точки
	Point(double x, double y);

	// Методы
	double getX() const;    // Получение координаты X

	double getY() const;    // Получение координаты Y

	void print() const;  // Для вывода точки

	double distance(const Point& other) const;         // Метод для вычисления расстояния от этой точки до другой

};
