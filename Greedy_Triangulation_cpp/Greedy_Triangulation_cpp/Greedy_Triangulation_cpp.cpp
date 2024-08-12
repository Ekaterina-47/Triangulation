// Greedy_Triangulation_cpp.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include "Point.h"
#include "Segment.h"
#include "Triangulation.h"
#include <random>

using namespace std;




// Функция для генерации точек на двумерном пространстве
vector<Point> generateRandomPoints(int N, double x_min = 0.0f, double x_max = 10.0f, double y_min = 0.0f, double y_max = 10.0f) {
    vector <Point> points;
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis_x(x_min, x_max);
    uniform_real_distribution<> dis_y(y_min, y_max);

    for (int i = 0; i < N; i++) {
        double x = dis_x(gen);
        double y = dis_y(gen);
        points.emplace_back(x, y);
    }

    return points;
}



int main()
{

    int N;
    cout << "Enter the num: ";
    cin >> N;

    if (N < 3) {
        cout << "Num must be > 2." << endl;
        return 1;
    }

    // Генерация точек на плоскости
    vector<Point> points = generateRandomPoints(N);

    cout << "Points: " << endl;
    for (int i = 0; i < points.size(); i++) {
        points[i].print();
        if (i < points.size() - 1) {
            cout << ", ";
        }
   }
    cout << endl << endl;

    // Создание объекта триангуляции
    Triangulation triangulation(points);

    // Вывод всех возможных отрезков триангуляции
    cout << "All segments:" << endl;
    triangulation.printSegments();

    // Выполнение триангуляции

    // Получение отрезков триангуляции

    // Вывод отрезков триангуляции

}

