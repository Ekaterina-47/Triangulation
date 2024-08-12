#include "Triangulation.h"

#include <iostream>
#include <algorithm>

using namespace std;

// Реализация конструктора и методов для класса Триангуляция


// Реализация конструктора
Triangulation::Triangulation(const vector<Point>& points) : points(points) {
	genSegments();    // Генерация
	sortSegments();   // Тут же происходит сортировка


}



// Генерация отрезков
void Triangulation::genSegments() {
	for (int i = 0; i < points.size(); i++) {
		for (int j = i + 1; j < points.size(); j++) {
			segments.emplace_back(points[i], points[j]);
		}
	}
}


// Cравнение отрезков по длинам
bool compareSegmentsByLength(const Segment& a, const Segment& b) {
	return a.getLength() < b.getLength();
}

// Метод для сортировки
void Triangulation::sortSegments() {
	sort(segments.begin(), segments.end(), compareSegmentsByLength);
}

// Вывод всех возможных отрезков среди точек
void Triangulation::printSegments() const {
	for (int i = 0; i < segments.size(); i++) {
		segments[i].printSegment();
		cout << endl;
	}
}


// Выполнение триангуляции
void Triangulation::makeTriangulation() {
	triangulation.push_back(segments[0]);  // Самый маленький отрезок помещается в список
	// Далее последовательная вставка отрезков в триангуляцию, если нет пересечений. Иначе, они отбрасываются.
	for (int i = 1; i < segments.size(); i++) {
		int iter = 0;   // переменная для отслеживания итерация по отрезкам триангуляции
		for (int j = 0; j < triangulation.size(); j++) {
			iter++;
			if (segments[i].intersection(triangulation[j]) == true) {
				break;
			}
		}
		// Если после всех итераций по отрезкам в триангуляции не возникло пересечения, то отрезок вставляется
		if (iter == triangulation.size()) {
			triangulation.push_back(segments[i]);
		}
	}
}

// Получение триангуляции
vector<Segment> Triangulation::getTriangulation() {
	return triangulation;
}

