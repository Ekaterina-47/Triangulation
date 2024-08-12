// Реализация конструктора и методов для класса Point

#include <iostream>
#include "Point.h"
#include <cmath>

using namespace std;


// Реализация конструктора
Point::Point(double x, double y) : x(x), y(y) {}


// Реализация метода getX
double Point::getX() const {
	return x;
}


// Реализация метода getY
double Point::getY() const{
	return y;
}

// Для вывода точек
void Point::print() const {
	cout << "(" << x << ", " << y << ")";
 }


// Реализация метода distance
double Point::distance(const Point& other) const {
	// Возвращается евклидово расстояние между данной точкой и другой
	return sqrt(pow(x - other.getX(), 2) + pow(y - other.getY(), 2));
}
