#pragma once

// ���������� ������ ��� �����

class Point {

private:

	double x;    // ���������� �� X
	double y;    // ���������� �� Y

public:
     
	// ����������� ��� �����
	Point(double x, double y);

	// ������
	double getX() const;    // ��������� ���������� X

	double getY() const;    // ��������� ���������� Y

	double distance(const Point& other) const;         // ����� ��� ���������� ���������� �� ���� ����� �� ������

};