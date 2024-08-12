#include "Segment.h"
#include <cmath>

using namespace std;

// ���������� ������������ � ������� ��� ������ Segment


// �����������
Segment::Segment(const Point& start, const Point& end) : start(start), end(end) {}



// �������� ������ �������
Point Segment::getStart() const{
	return start;
}

// �������� ����� �������
Point Segment::getEnd() const {
	return end;
}

// ���������� ������ �������
double Segment::getLength() const {
	return start.distance(end);
}


// �������� �� ����������� � ������ ��������
	bool Segment::intersection(const Segment & other) const {
		double x1 = start.getX(), y1 = start.getY();
		double x2 = end.getX(), y2 = end.getY();
		double x3 = other.getStart().getX(), y3 = other.getStart().getY();
		double x4 = other.getEnd().getX(), y4 = other.getEnd().getY();

		double denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);

		if (denominator == 0) {
			return false;        // ������� ����������� ��� �����������
		}

		double t_a = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator;
		double t_b = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator;

		// �������� �� ����������� �������� ������ ����� ������
		if (0 < t_a && t_a < 1 && 0 < t_b && t_b < 1) {
			return true;
		}
		else
		{
			return false;
		}
	}