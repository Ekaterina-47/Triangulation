// ���������� ������������ � ������� ��� ������ Point

#include "Point.h"
#include <cmath>

using namespace std;


// ���������� ������������
Point::Point(double x, double y) : x(x), y(y) {}


// ���������� ������ getX
double Point::getX() const {
	return x;
}


// ���������� ������ getY
double Point::getY() const{
	return y;
}


// ���������� ������ distance
double Point::distance(const Point& other) const {
	// ������������ ��������� ���������� ����� ������ ������ � ������
	return sqrt(pow(x - other.getX(), 2) + pow(y - other.getY(), 2));
}
