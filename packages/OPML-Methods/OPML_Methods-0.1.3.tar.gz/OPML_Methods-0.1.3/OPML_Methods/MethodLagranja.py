import numexpr as ne
import sympy
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import re


class MethodLagranja:
    def find(self, x: str, y: str, x_y, f, z, x_from, x_to, y_from, y_to, left_x_y):
        """

        Функция находит экстермумы, седловые точки и точки дальнейшего исследования
        по методу лагранжа и строит 3Д график

        Parameters
        ===========
        :param x: str
            символ х
        :param y: str
            символ у
        :param x_y:
            ограничивающая функция (пример: x**2+y**2-10)
        :param f:
            строковая функция f(x, y)
        :param z: str
            строковая функция f(x, y) + (лямбда) * (ограничивающую функцию)
        :param x_from: float
            интервал "от" по х
        :param x_to: float
            интервал "до" по х
        :param y_from: float
            интервал "от" по у
        :param y_to: float
            интервал "до" по у
        :param left_x_y
            левая часть ограничивающей функции x_y
        Returns
        ===========
        3Д график с отмеченными точкам
        """

        # Преобразуем произвольное выражение в тип, который можно использовать внутри SymPy
        L = symbols('L')
        func = sympify(z)


        func_ogr_y = str(solve(x_y, y)[0])

        values_diff = solve([func.diff(x), func.diff(y), x_y], [x, y, L], dict=True)

        # проверяем есть ли пара в словаре для икса и игрика и при ее отсутствии добавляем
        a = 0
        for i in range(len(values_diff)):
            if len(values_diff[i]) == 2:
                a = 1
                values_diff[i].update(dict(n=0))

        # Считаем первые производные по х и у и приравниваем их к нулю чтобы найти эти х и у

        v_d = []
        for i in range(len(values_diff)):  # список для каждой отдельной точки
            v_d_in = []
            for key, value in values_diff[i].items():
                v_d_in.append(value)
            v_d.append(v_d_in)

        values_diff = v_d


        if a == 1:
            for i in range(len(values_diff)):
                values_diff[i].append(values_diff[i][0])
                values_diff[i].pop(0)
            for i in range(len(values_diff)):
                values_diff[i][0] = values_diff[i][0].subs(y, values_diff[i][1])

        points_max = []
        points_min = []
        point_l_max = []
        point_l_min = []

        for i in range(len(values_diff)):
            if (values_diff[i][0] >= x_from) and (values_diff[i][0] <= x_to) and (values_diff[i][1] >= y_from) and (values_diff[i][1] <= y_to):
                second_diff = (func.diff(x).diff(x) + 2 * func.diff(x).diff(y) + func.diff(y).diff(y)).subs(L, values_diff[i][2])

                if second_diff < 0:
                    points_max.append([values_diff[i][0], values_diff[i][1]])
                    point_l_max.append(values_diff[i][2])

                elif second_diff > 0:
                    points_min.append([values_diff[i][0], values_diff[i][1]])
                    point_l_min.append(values_diff[i][2])


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
##
        # Построение списков точек минимума для графика
        all_points_x = []
        all_points_y = []
        all_points_z = []
#
        lst_points_x_min = []
        lst_points_y_min = []
        for i in range(len(points_min)):
            if points_min:
                lst_points_x_min.append(float(points_min[i][0]))
                lst_points_y_min.append(float(points_min[i][1]))
                # Считаем точки по x и y для центрирования по графику
                all_points_x.append(float(points_min[i][0]))
                all_points_y.append(float(points_min[i][1]))
                all_points_z.append(float(func.subs([(x, float(points_min[i][0])), (y, float(points_min[i][1])), (L, float(point_l_min[i]))])))
#
        lst_points_z_min = []
#
        for i in range(len(lst_points_x_min)):
            lst_points_z_min.append(float(func.subs([(x, lst_points_x_min[i]), (y, lst_points_y_min[i]), (L, float(point_l_min[i]))])))
#
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
                all_points_z.append(float(func.subs([(x, float(points_max[i][0])), (y, float(points_max[i][1])), (L, float(point_l_max[i]))])))

        lst_points_z_max = []

        for i in range(len(lst_points_x_max)):
            lst_points_z_max.append(float(func.subs([(x, lst_points_x_max[i]), (y, lst_points_y_max[i]), (L, float(point_l_max[i]))])))

        z_from = -20
        z_to = 20
        # Среднее x, y для центрирования
        if points_max or points_min:
            mean_x = np.mean(all_points_x)
            mean_y = np.mean(all_points_y)
            mean_z = np.mean(all_points_z)
            length_x = mean_x + abs(max(all_points_x) - mean_x) + abs(max(all_points_x) - min(all_points_x))/5 + 1
            length_y = mean_y + abs(max(all_points_y) - mean_y) + abs(max(all_points_y) - min(all_points_y))/5 + 1
            length_z = mean_z + abs(max(all_points_z) - mean_z) + abs(max(all_points_z) - min(all_points_z))/5 + 3
            x_from = mean_x - length_x
            x_to = mean_x + length_x
            y_from = mean_y - length_y
            y_to = mean_y + length_y
            z_from = mean_z - length_z
            z_to = mean_z + length_z


        # Подпись осей

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title('Поиск экстремумов')
        ax.set_zlabel('Z')
        ax.set_ylabel('Y')
        ax.set_xlabel('X')

        x = np.linspace(x_from, x_to, 25)
        y = np.linspace(y_from, y_to, 25)
        x, y = np.meshgrid(x, y)
        Z = ne.evaluate(f)

        surf = ax.plot_surface(x, y, Z, cmap='viridis', shade=True, alpha=0.5)
        fig.colorbar(surf, shrink=0.5, aspect=10)


        if points_max or points_min:
            if 'x**2' in x_y:
                x = np.linspace(-50, 50, 10000)
                Z = np.linspace(z_from, z_to, 25)
                Xc, Zc = np.meshgrid(x, Z)
                Yc =  ne.evaluate(func_ogr_y)
                ax.plot_wireframe(Xc, Yc, Zc, color='black', alpha = 0.3)
                ax.plot_wireframe(Xc, -Yc, Zc, color='black',alpha = 0.3)
            else:
                x = np.linspace(x_from, x_to, 25)
                y = np.linspace(y_from, y_to, 25)
                x, y = np.meshgrid(x, y)
                Z = ne.evaluate(left_x_y)
                ax.plot_wireframe(x, y, Z, color='black', alpha=0.3)


        # Рисуем на графике точки минимума и максимума
        for i in range(len(lst_points_x_min)):
            ax.scatter(lst_points_x_min[i], lst_points_y_min[i], lst_points_z_min[i], c='r', s=50,
                       label=f'Точка минимума {lst_points_x_min[i], lst_points_y_min[i], lst_points_z_min[i]}')

        # Рисуем на графике точки максимума
        for i in range(len(lst_points_x_max)):
            ax.scatter(lst_points_x_max[i], lst_points_y_max[i], lst_points_z_max[i], c='b', s=50,
                       label=f'Точка максимума {lst_points_x_max[i], lst_points_y_max[i], lst_points_z_max[i]}')
        #
            # Рисуем легенду
        if points_max or points_min:
            if not points_max:
                ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Точки максимума не найдены')
            if not points_min:
                ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Точки минимума не найдены')
            ax.legend(labelcolor='black')
        else:

            ax.scatter(0, 0, 0, c='w', s=0.1, label=f'Никакие точки не найдены')
            ax.legend(labelcolor='black')

        plt.show()




