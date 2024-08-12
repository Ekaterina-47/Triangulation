#pragma once
#include "Point.h"

using namespace std;


// ���������� ������ ��� ��������
class Segment {

private:
	Point start;
	Point end;

	double segmentLength;

public:

	// ����������� ��� �������
	Segment(const Point& start, const Point& end);

	// ������

	Point getStart() const;      // �������� ��������� �����
	Point getEnd() const;        // �������� �������� �����

	double getLength() const;                        // ���������� ������ �������
	bool intersection(const Segment& other) const;   // �������� �� ����������� � ������ ��������
};