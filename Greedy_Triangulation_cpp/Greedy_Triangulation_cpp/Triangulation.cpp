#include "Triangulation.h"

using namespace std;

// Реализация конструктора и методов для класса Триангуляция


// Реализация конструктора
Triangulation::Triangulation(const vector<Point>& points) : points(points) {}



// Генерация отрезков
void Triangulation::genSegments() {
	for (int i = 0; i < points.size(); i++) {
		for (int j = i + 1; j < points.size(); j++) {
			segments.emplace_back(points[i], points[j]);
		}
	}
}


// Метод для сортировки
void Triangulation::sortSegments() {
	//
}


// Выполнение триангуляции
void Triangulation::makeTriangulation() {
	//
}

// Получение триангуляции
vector<Segment> Triangulation::getTriangulation() {
	//
}

