import numexpr as ne
import sympy
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
# import re
# from matplotlib import cm
# from mpl_toolkits.axes_grid1 import make_axes_locatable


class SearchExtremes:
    def find(self, x: str, y: str, z: str, x_from: float, x_to: float, y_from: float, y_to: float):
        """
        Функция находит экстермумы, седловые точки и точки дальнейшего исследования и строит 3Д график

        Parameters
        ===========
        :param x: str
            символ х
        :param y: str
            символ у
        :param z: str
            строковая функция
        :param x_from: float
            интервал "от" по х
        :param x_to: float
            интервал "до" по х
        :param y_from: float
            интервал "от" по у
        :param y_to: float
            интервал "до" по у

        Returns
        ===========
        3Д график с отмеченными точками экстремумов
        """

        # Преобразуем произвольное выражение в тип, который можно использовать внутри SymPy
        func = sympify(z)
        # Считаем первые производные по х и у и приравниваем их к нулю чтобы найти эти х и у
        values_diff = solve([func.diff(x), func.diff(y)], dict=True)  # делаем это все словарем (dict=True)
        v_d = []

        # проверяем есть ли пара в словаре для икса и игрика и при ее отсутствии добавляем
        for i in range(len(values_diff)):
            if (len(values_diff[i]) == 1) and (value == 0 for value in values_diff[i].values()):
                values_diff[i].update(dict(n=0))


        # заводим цикл по длине values_diff, чтобы избавиться от значений словаря
        for i in range(len(values_diff)):
            v_d_in = []  # список для каждой отдельной точки
            for key, value in values_diff[i].items():
                v_d_in.append(value)

            if (type(v_d_in[0]) != int) and (type(v_d_in[1]) != int):
                if ((v_d_in[0]).has(I) is False) and ((v_d_in[1]).has(I) is False):  # проверяем на налич комплекс чисел
                    v_d_in[0] = float(v_d_in[0])  # Переводим во float для удобства
                    v_d_in[1] = float(v_d_in[1])
                    v_d.append(v_d_in)
        values_diff = v_d  # список точек, где на первом месте х, на втором у

        # Создаем гессиан
        ges = np.array([[func.diff(x).diff(x), func.diff(x).diff(y)],
                        [func.diff(y).diff(x), func.diff(y).diff(y)]])

        points_max = []  # список максимумов
        points_min = []  # список минимумов
        points_not_defined = []  # список точек требующих доп исследования
        saddle_point = []  # список седловых точек

        for i in range(len(values_diff)):  # создаем цикл перебирающий каждую точку

            # проверяем значения гессиана (a, b, c) на то что они являются числами и если да, то считаем их,
            # а если нет то идем дальше
            if (type(ges[0][0]) == sympy.core.numbers.Integer) or (type(ges[0][0]) == sympy.core.numbers.Zero):
                a = ges[0][0]
            else:
                a = func.diff(x).diff(x).subs([(x, values_diff[i][0]), (y, values_diff[i][1])])
            if (type(ges[0][1]) == sympy.core.numbers.Integer) or (type(ges[0][1]) == sympy.core.numbers.Zero):
                b = ges[0][1]
            else:
                b = func.diff(x).diff(y).subs([(x, values_diff[i][0]), (y, values_diff[i][1])])
            if (type(ges[1][1]) == sympy.core.numbers.Integer) or (type(ges[1][1]) == sympy.core.numbers.Zero):
                c = ges[1][1]
            else:
                c = func.diff(y).diff(y).subs([(x, values_diff[i][0]), (y, values_diff[i][1])])

            # проверка на существование локальных экстремумов по формуле (a * c - b ** 2) > 0

            if (values_diff[i][0] >= x_from) and (values_diff[i][0] <= x_to) and (values_diff[i][1] >= y_from) and (
                    values_diff[i][1] <= y_to):
                if (a * c - b ** 2) > 0:

                    if a > 0:
                        # Локальный экстремум(минимум)
                        points_min.append((values_diff[i][0], values_diff[i][1]))
                    elif a < 0:
                        # Локальный экстремум(максимум)
                        points_max.append((values_diff[i][0], values_diff[i][1]))
                elif (a * c - b ** 2) == 0:
                    # Требуется дополнительное исследование (a*c-b**2) = 0
                    points_not_defined.append((values_diff[i][0], values_diff[i][1]))

                # Седловая точка
                if ((a > 0) and (a * c < 0)) or ((a < 0) and (a * c < 0)):
                    saddle_point.append((values_diff[i][0], values_diff[i][1]))

        # если нет локального экстремума выводим запись о его отсутствии, если есть выводим точки
        # аналогично с точкой доп исследования и с седловой
        #if not points_max:
        #    print("Локального экстремума (максимума) нет")
        #else:
        #    print("Локальный экстремум (максимум)")
        #    for i in range(len(points_max)):
        #        print(points_max[i])
        #if not points_min:
        #    print("Локального экстремума (минимума) нет")
        #else:
        #    print("Локальный экстремум (минимум)")
        #    for i in range(len(points_min)):
        #        print(points_min[i])
        #if not points_not_defined:
        #    print("Дополнительное исследование не требуется")
        #else:
        #    print("Требуется дополнительное исследование")
        #    for i in range(len(points_not_defined)):
        #        print(points_not_defined[i])
        #if not saddle_point:
        #    print("Седловой точки нет")
        #else:
        #    print("Седловая точка")
        #    for i in range(len(saddle_point)):
        #        print(saddle_point[i])

        # Для 3д графика
        # Построение списков точек минимума для графика

        all_points_x = []
        all_points_y = []

        lst_points_x_min = []
        lst_points_y_min = []
        for i in range(len(points_min)):
            if points_min:
                lst_points_x_min.append(float(points_min[i][0]))
                lst_points_y_min.append(float(points_min[i][1]))
                # Считаем точки по x и y для центрирования по графику
                all_points_x.append(float(points_min[i][0]))
                all_points_y.append(float(points_min[i][1]))

        lst_points_z_min = []

        for i in range(len(lst_points_x_min)):
            lst_points_z_min.append(float(func.subs([(x, lst_points_x_min[i]), (y, lst_points_y_min[i])])))

        # Построение списков точек максимума для графика
        lst_points_x_max = []
        lst_points_y_max = []
        for i in range(len(points_max)):
            if points_max:
                lst_points_x_max.append(float(points_max[i][0]))
                lst_points_y_max.append(float(points_max[i][1]))
                # Считаем точки по x и y для центрирования по графику
                all_points_x.append(float(points_max[i][0]))
                all_points_y.append(float(points_max[i][1]))

        lst_points_z_max = []

        for i in range(len(lst_points_x_max)):
            lst_points_z_max.append(float(func.subs([(x, lst_points_x_max[i]), (y, lst_points_y_max[i])])))

        # Построение списков седловой точки
        lst_points_x_saddle = []
        lst_points_y_saddle = []
        lst_points_z_saddle = []

        for i in range(len(saddle_point)):
            if saddle_point:
                lst_points_x_saddle.append(float(saddle_point[i][0]))
                lst_points_y_saddle.append(float(saddle_point[i][1]))
                # Считаем точки по x и y для центрирования по графику
                all_points_x.append(float(saddle_point[i][0]))
                all_points_y.append(float(saddle_point[i][1]))

        for i in range(len(lst_points_x_saddle)):
            lst_points_z_saddle.append(float(func.subs([(x, lst_points_x_saddle[i]), (y, lst_points_y_saddle[i])])))

        # Построение списков точки доп исследования
        lst_points_x_dop = []
        lst_points_y_dop = []
        lst_points_z_dop = []

        for i in range(len(points_not_defined)):
            if points_not_defined:
                lst_points_x_dop.append(float(points_not_defined[i][0]))
                lst_points_y_dop.append(float(points_not_defined[i][1]))
                # Считаем точки по x и y для центрирования по графику
                all_points_x.append(float(points_not_defined[i][0]))
                all_points_y.append(float(points_not_defined[i][1]))

        for i in range(len(lst_points_x_dop)):
            lst_points_z_dop.append(float(func.subs([(x, lst_points_x_dop[i]), (y, lst_points_y_dop[i])])))

        # Среднее x, y для центрирования
        if points_not_defined or saddle_point or points_max or points_min:
            mean_x = np.mean(all_points_x)
            mean_y = np.mean(all_points_y)
            length_x = mean_x + abs(max(all_points_x) - mean_x) + abs(max(all_points_x) - min(all_points_x))/5 + 1
            length_y = mean_y + abs(max(all_points_y) - mean_y) + abs(max(all_points_y) - min(all_points_y))/5 + 1
            x_from = mean_x - length_x
            x_to = mean_x + length_x
            y_from = mean_y - length_y
            y_to = mean_y + length_y


        # Подпись осей
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='3d')
        ax.set_title('Поиск экстремумов')
        ax.set_zlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')

        x = np.linspace(x_from,x_to, 25)
        y = np.linspace(y_from,y_to, 25)
        x, y = np.meshgrid(x, y)
        Z = ne.evaluate(z)

        surf = ax.plot_surface(x, y, Z, cmap='viridis', shade=True, alpha=0.5)
        fig.colorbar(surf, shrink=0.5, aspect=10)

        # Рисуем на графике точки минимума и максимума
        for i in range(len(lst_points_x_min)):
            ax.scatter(lst_points_x_min[i], lst_points_y_min[i], lst_points_z_min[i], c='r', s=50,
                       label=f'Точка минимума {lst_points_x_min[i], lst_points_y_min[i], lst_points_z_min[i]}')

        # Рисуем на графике точки максимума
        for i in range(len(lst_points_x_max)):
            ax.scatter(lst_points_x_max[i], lst_points_y_max[i], lst_points_z_max[i], c='b', s=50,
                       label=f'Точка максимума {lst_points_x_max[i], lst_points_y_max[i], lst_points_z_max[i]}')

        # Рисуем на графике седловые точки
        for i in range(len(lst_points_x_saddle)):
            ax.scatter(lst_points_x_saddle[i], lst_points_y_saddle[i], lst_points_z_saddle[i], c='black', s=50,
                       label=f'Седловая точка {lst_points_x_saddle[i], lst_points_y_saddle[i], lst_points_z_saddle[i]}')

        # Рисуем на графике точки доп исследования
        for i in range(len(lst_points_x_dop)):
            ax.scatter(lst_points_x_dop[i], lst_points_y_dop[i], lst_points_z_dop[i], c='g', s=50,
                       label=f'Точка, требующая доп исследований {lst_points_x_dop[i], lst_points_y_dop[i], lst_points_z_dop[i]}')

        # Рисуем легенду
        if points_max or points_min or saddle_point or points_not_defined:
            if not points_max:
                ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Точки максимума не найдены')
        if not points_min:
            ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Точки минимума не найдены')
        if not saddle_point:
            ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Седловые точки не найдены')
        if not points_not_defined:
            ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Точки для дальнейшего исследования не найдены')
            ax.legend(labelcolor='black')
        else:
            ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Никакие точки не найдены')
            ax.legend(labelcolor='black')

        plt.show()
