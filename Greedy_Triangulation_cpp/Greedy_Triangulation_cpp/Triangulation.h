#pragma once

#include "Point.h"
#include "Segment.h"
#include <vector>

using namespace std;

class Triangulation {

private:
	vector<Point> point;             // ������ �����
	vector<Segment> segment;         // ������ ��������
	vector<Segment> triangulation;   // ������ �������� �������� ������������

	// ��������� ���� ��������� ��������
	void genSegments();

	// ���������� ��������
	void sortSegments();

public:
	// �����������, ��������� ������ �����
	Triangulation(const vector<Point>& points);

	// ���������� ������������
	void makeTriangulation();

	// ��������� �������� ������������
	vector<Segment> getTriangulation() const;
};