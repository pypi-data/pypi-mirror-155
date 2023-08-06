import pandas as pd
from sympy import *
import re
import numpy as np


class GradDesentConstStep:
    def find(self, z, l, x, iter, e, flag1, flag2, extr):
        """
        Функция находит экстремум методом градиентного спуска с постоянным шагом.
        Parameters
        ===========
        :param z: str
            функция минимизации (максимизации)
        :param l: float
            шаг
        :param x: float
            начальная точка, из которой начинаем спуск
        :param iter: int
            число итераций
        :param e: float
            точность оптимизации
        :param flag1: int
            Вывод промежуточных результатов? 1 - да / 0 - нет
        :param flag2: int
            запись промежуточных результатов в датасет 1 - да / 0 - нет
        :param extr: int
            экстремум который вы хотите найти 1 - максимум, 0 - минимум
        :return:
            Возвращает точку максимума или минимума, значение функции в точке минимума и датасет с промежуточными
             вычислениями
        """
        func = sympify(z)

        lst_xi = np.sort(list(set(re.findall(r'[x]\d', z))))

        det_func = []
        for i in range(len(lst_xi)):
            det_func.append(func.diff(lst_xi[i]))
        i = 0

        df = pd.DataFrame(columns=['Номер итерации', 'Полученные значения'])

        while i < iter:
            podst = []
            calc_det = []
            for j in range(len(lst_xi)):
                podst.append((lst_xi[j], x[j][0]))
            for j in range(len(lst_xi)):
                calc_det.append([det_func[j].subs(podst)])

            xk = x - np.dot(l, calc_det)
            podst_after = []
            for j in range(len(lst_xi)):
                podst_after.append((lst_xi[j], xk[j][0]))
            x = xk
            x_beauty = []
            # Написать датасеты использовать x_beauty
            for j in range(len(x)):
                x_beauty.append(float(x[j][0]))
            if flag1 == 1:
                print(f'Итерация №{i}, точка {tuple(x_beauty)}')
            if flag2 == 1:
                df.loc[i] = [i, tuple(x_beauty)]

            if extr == 0:
                if func.subs(podst_after) > func.subs(podst):
                    print(f'Минимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке минимума {float(func.subs(podst))}')
                    print(f'Неточное решение. При следующем запуске уменьшите лямбду.')
                    break
                elif abs(func.subs(podst) - func.subs(podst_after)) < e:
                    print(f'Минимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке минимума {float(func.subs(podst_after))}')
                    break

                elif i == (iter - 1):
                    print(f'Неточное решение. На последней итерации минимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке минимума {float(func.subs(podst_after))}')
                    break
            else:
                if func.subs(podst_after) > func.subs(podst):
                    print(f'Максимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке максимума {float(func.subs(podst))}')
                    print(f'Неточное решение. При следующем запуске уменьшите лямбду.')
                    break
                elif abs(func.subs(podst) - func.subs(podst_after)) < e:
                    print(f'Максимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке максимума {float(func.subs(podst_after))}')
                    break

                elif i == (iter - 1):
                    print(f'Неточное решение. На последней итерации максимум в точке {tuple(x_beauty)}')
                    print(f'Значение функции в точке максимума {float(func.subs(podst_after))}')
                    break

            i += 1

        if flag2 == 1:
            print(df)
            df.to_csv('GradDesentConstStep_results.csv', index=False)
            print('Датасет сохранен в папку проекта в формате csv')


# while True:
#     print("Какой экстремум вы хотите найти? 1 - максимум \ 0 - минимум")
#     q = int(input())
#     if q == 1:
#         extr = 1
#         break
#     elif q == 0:
#         extr = 0
#         break
#     else:
#         print("Такой команды нет. Введите снова")
# print("Введите функцию f(x1, x2, ... , xn). Например: x1**2 + x1*x2**3 + x3**2")
# f = input()
# if extr == 1:
#     f = "- (" + f + ")"
#     print(f)
# count_param = np.sort(list(set(re.findall(r'[x]\d', f))))
# print("Введите шаг. Например: 0.01")
# l = float(input())
# print("Введите начальную точку, из которой начинаем спуск.")
# lst_xi = []
# for i in range(len(count_param)):
#     print(f'Введите {count_param[i]}. Например: 1')
#     xi = [float(input())]
#     lst_xi.append(xi)
# while True:
#     print("Хотите ввести число итераций? 1 - да / 0 - нет")
#     q = int(input())
#     if q == 1:
#         print("Введите кол-во итераций. Например: 500")
#         iter = int(input())
#         break
#     elif q == 0:
#         iter = 500
#         break
#     else:
#         print("Такой команды нет. Введите снова")
# while True:
#     print("Хотите ввести точность оптимизации? 1 - да / 0 - нет")
#     q = int(input())
#     if q == 1:
#         print("Введите точность оптимизации. Например: 0.001")
#         e = float(input())
#         break
#     elif q == 0:
#         e = 0.0001
#         break
#     else:
#         print("Такой команды нет. Введите снова")
#
# while True:
#     print("Хотите ввести промежуточные результаты? 1 - да / 0 - нет")
#     q = int(input())
#     if q == 1:
#         flag1 = 1
#         break
#     elif q == 0:
#         flag1 = 0
#         break
#     else:
#         print("Такой команды нет. Введите снова")
#
# while True:
#     print("Хотите записать промежуточные результаты в датасет? 1 - да / 0 - нет")
#     q = int(input())
#     if q == 1:
#         flag2 = 1
#         break
#     elif q == 0:
#         flag2 = 0
#         break
#     else:
#         print("Такой команды нет. Введите снова")
#
# function = GradDesentConstStep()
# function.find(f, l, lst_xi, iter, e, flag1, flag2, extr)
