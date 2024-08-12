#pragma once

#include "Point.h"
#include "Segment.h"
#include <vector>

using namespace std;

class Triangulation {

private:
	vector<Point> point;             // Список точек
	vector<Segment> segment;         // Список отрезков
	vector<Segment> triangulation;   // Список итоговых отрезков триангуляции

	// Генерация всех возможных отрезков
	void genSegments();

	// Сортировка отрезков
	void sortSegments();

public:
	// Конструктор, принимает список точек
	Triangulation(const vector<Point>& points);

	// Выполнение триангуляции
	void makeTriangulation();

	// Получение отрезков триангуляции
	vector<Segment> getTriangulation() const;
};