#pragma once

#include "Point.h"
#include "Segment.h"
#include <vector>

using namespace std;

class Triangulation {

private:
	vector<Point> points;             // Список точек
	vector<Segment> segments;         // Список отрезков
	vector<Segment> triangulation;   // Список итоговых отрезков триангуляции

public:
	// Конструктор, принимает список точек
	Triangulation(const vector<Point>& points);

	// Генерация всех возможных отрезков
	void genSegments();

	// Сортировка отрезков
	void sortSegments();

	// Выполнение триангуляции
	void makeTriangulation();

	// Получение отрезков триангуляции
	vector<Segment> getTriangulation();

};
