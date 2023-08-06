from sklearn.datasets import make_classification
from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import numexpr as ne
import copy
from re import findall

from .MethodLagranja import *
from .SearchExtremes import *
from .BFGS import *
from .PorabolMet import *
from .AdjointGrad import *
from .FastGradDesent import *
from .GradDesentConstStep import *
from .GradDesentDrobStep import *
from .LinRegr import *
from .PolRegres import *
from .ExpRegres import *
from .BrentMet_var2 import *
from .Newton import *
from .Pryam import *
from .Pryam_dvoy import *
from .input_validation import check_expression, check_restr, check_point
from .prepocessing import prepare_all
from .Сlassification import Сlassification

class User:
    def UserPrint():
        print("Какой модуль вас интересует? \n"
              "1. Поиск экстремума функции нескольких переменных. \n"
              "     Функции модуля : \n"
              "         1.1. Поиск локальных экстремумов функции двух переменных. \n"
              "         1.2. Поиск локальных экстремумов функции двух переменных с ограничениями (метод Лагранжа).\n"
              "2. Методы одномерной оптимизации. \n"
              "     Функции модуля : \n"
              "         2.1. Поиск экстремума функции одной переменной методом золотого сечения. \n"
              "         2.2. Поиск экстремума функции одной переменной методом парабол. \n"
              "         2.3. Поиск экстремума функции одной переменной комбинированным методом Брента. \n"
              "         2.4. Алгоритм неточной одномерной минимизации(Алгоритм Бройдена-Флетчера-Гольдфарба-Шанно). \n"
              "3. Методы многомерной оптимизации. \n"
              "     Функции модуля : \n"
              "         3.1. Поиск экстремума функции многих переменных методом градиентного спуска с"
              " постоянным шагом. \n"
              "         3.2. Поиск экстремума функции многих переменных методом градиентного спуска с"
              " дроблением шага. \n"
              "         3.3. Поиск экстремума функции многих переменных методом наискорейшего градиентного спуска. \n"
              "         3.4. Поиск экстремума функции многих переменных при помощи алгоритма Ньютона - сопряженного"
              " градиента. \n"
              "4. Регрессия. \n"
              "     Функции модуля : \n"
              "         4.1. Функция, реализующая модель линейной регрессии и 3 видами регуляторов:"
              " L1, L2 и Стьюдента. \n"
              "         4.2. Функция, реализующая модель полиномиальной регрессии и 3 видами регуляторов:"
              " L1, L2 и Стьюдента. \n"
              "         4.3. Функция, реализующая модель экспоненциальной регрессии и 3 видами регуляторов:"
              " L1, L2 и Стьюдента. \n"
              "5. Метод внутренней точки. \n"
              "     Функции модуля : \n"
              "         5.1. Решение задачи оптимизации для функции с ограничениями типа"
              " равенства методом Ньютона (способ  решения двойственной задачи). \n"
              "         5.2. Решение задачи оптимизации для функции с ограничениями типа"
              " неравенства методом логарифмических барьеров (прямой метод внутренней точки). \n"
              "         5.3. Решение задачи оптимизации для функции с ограничениями типа"
              " неравенства прямо-двойственным методом внутренней точки. \n"
              "6. Логистическая регрессия, обучение SVM при помощи прямо-двойственного метода внутренней точки. \n"
              "     Функции модуля : \n"
              "         6.1. Функция, реализующую модель классификации на два класса на основе логистической"
              " регрессии. \n"
              "         6.2. Функция, реализующая модель классификации на два класса на основе"
              " логистической регрессии с радиальными базисными функциями. \n"
              "         6.3. Функция, реализующая модель классификации на два класса на основе"
              " логистической регрессии с регуляризацией L1. \n"
              "         6.4. Функция, реализующая модель классификации на два класса на основе"
              " метода опорных векторов. \n"
              "7. Методы отсекающих плоскостей. \n"
              "     Функции модуля : \n"
              "         7.1. Функция, решающая задачу целочисленного линейного программирования"
              " методом отсекающих плоскостей ( Метод Гомори). \n"
              "         7.2. Функция, решающая задачу целочисленного линейного программирования"
              " методом полного перебора ( Метод ветвей и границ). \n"
              "8. Методы стохастической оптимизации. \n"
              "     Функции модуля : \n"
              "         8.1. Функция, решающая задачу поиска экстремума функции методом"
              " стохастического градиентного спуска (SGD). \n"
              "         8.2. Функция, реализующая модель классификации на два класса методом"
              " опорных векторов SVM с применением алгоритма градиентного спуска для минимизации"
              " функции ошибок (PEGASOS algorithm) \n"
              "         8.3. Функция, решающая задачу поиска экстремума функции методом имитации отжига. \n"
              "         8.4. Функция, решающая задачу поиска экстремума функции при помощи генетического алгоритма.")


        print("Введите функцию которую вы ходите использовать, например 1.1:")
        userInput = input()
        if userInput == "1.1":
            x, y = symbols('x y')
            print("Введите функцию f(x, y). Например:  x**2 + y ** 2 + 1")
            f = input()
            # x/y+x**2+y**3
            # exp(x+y)*(x**2-2*y**2)
            # x**2 + y ** 2 + 1
            print('Есть ли ограничения по x и y? 1-да / 0 – нет')
            ogr = int(input())
            x_from, x_to, y_from, y_to = -10, 10, -10, 10
            if ogr == 1:
                print('Введите допустимые интервалы по x:')
                print("Введите точку от. Пример: -10")
                x_from = float(input())
                print("Введите точку до. Пример: 10")
                x_to = float(input())

                print('Введите допустимые интервалы по y:')
                print("Введите точку от. Пример: -10")
                y_from = float(input())
                print("Введите точку до. Пример: 10")
                y_to = float(input())
            functions1 = SearchExtremes()
            functions1.find(x, y, f, x_from, x_to, y_from, y_to)
        elif userInput == "1.2":
            x, y = 'x', 'y'
            print("Введите функцию f(x, y). Например:  4*y**2 + x**2")

            f = input()
            # 5 - 3*x - 4*y
            # x + 3*y
            # 5*x*y - 4
            print("Ввод условия(ограничения).")
            print("Введите левую часть ограничения. Например: x**2 + y**2")
            left_x_y = input()
            print("Введите правую часть ограничения. Например: 25")
            # x**2 + y**2
            # (x**2)/8 + (y**2)/2
            right_x_y = input()
            x_y = left_x_y + '-' + right_x_y

            f_x_y = f + ' + L * (' + x_y + ')'
            print('Есть ли ограничения по x и y? 1-да / 0 – нет')
            ogr = int(input())
            x_from, x_to, y_from, y_to = -30, 30, -30, 30
            if ogr == 1:
                print('Введите допустимые интервалы по x:')
                print("Введите точку от. Пример: -10")
                x_from = float(input())
                print("Введите точку до. Пример: 10")
                x_to = float(input())

                print('Введите допустимые интервалы по y:')
                print("Введите точку от. Пример: -10")
                y_from = float(input())
                print("Введите точку до. Пример: 10")
                y_to = float(input())
            functions1 = MethodLagranja()
            functions1.find(x, y, x_y, f, f_x_y, x_from, x_to, y_from, y_to, left_x_y)
        elif userInput == "2.1":
            print("Введите функцию f(x, y). Например:  -5*x**5 + 4*x**4 - 12* x**3 + 11*x**2 - 2*x - 1")
            f = input()
            print('Есть ли ограничения по x? 1-да / 0 – нет')
            org = int(input())
            Xl, Xu = -10, 10
            if org == 1:
                print("Введите левое ограничение по x. Например: -0.5")
                Xl = float(input())
                print("Введите правое ограничение по x. Например: 0.5")
                Xu = float(input())
            print("Хотите указать e(точность)? 1 - да / 0 - нет")
            ep = int(input())
            e = 10 ** (-5)
            if ep == 1:
                print("Введите e. Например: 0.001")
                e = float(input())
            ea = 500
            print("Хотите увидеть промежуточные рузльтаты поиск экстремума? 1 - да / 0 - нет")
            while True:
                answ = int(input())
                if answ == 1:
                    flag = 'True'
                    break
                elif answ == 0:
                    flag = 'False'
                    break
                else:
                    print("Такого ответа нет! Введите корректно.")
            print("Хотите указать кол-во итераций? 1 - да / 0 - нет")
            it = int(input())
            iter = 500
            if it == 1:
                print("Введите кол-во итераций. Например: 10")
                iter = int(input())
            functions = GoldenSection()
            print(functions.find(f, Xl, Xu, e, ea, flag, iter))
        elif userInput == "2.2":
            print("Введите функцию f(x, y). Например:  3*x*sin(0.75*x) + exp(-2*x)")
            f = input()
            print('Есть ли ограничения по x? 1-да / 0 – нет')
            org = int(input())
            Xl, Xu = -10, 10
            if org == 1:
                print("Введите левое ограничение по x. Например: 0")
                Xl = float(input())
                print("Введите правое ограничение по x. Например: 6")
                Xu = float(input())
            print("Хотите указать e(точность)? 1 - да / 0 - нет")
            ep = int(input())
            e = 10 ** (-5)
            if ep == 1:
                print("Введите e. Например: 0.001")
                e = float(input())
            print("Хотите увидеть промежуточные рузльтаты поиска экстремума? 1 - да / 0 - нет")
            while True:
                answ = int(input())
                if answ == 1:
                    flag = 1
                    break
                elif answ == 0:
                    flag = 0
                    break
                else:
                    print("Такого ответа нет! Введите корректно.")
            print("Хотите указать кол-во итераций? 1 - да / 0 - нет")
            it = int(input())
            iter = 500
            if it == 1:
                print("Введите кол-во итераций. Например: 10")
                iter = int(input())
            functions = PorabolMet()
            functions.find(f, Xl, Xu, e, flag, iter)
        elif userInput == "2.3":
            print("Введите функцию f(x). Например:  3*x*sin(0.75*x) + exp(-2*x)")
            y = input()
            print("Введите левое ограничение по x. Например: 0")
            a = float(input())
            print("Введите правое ограничение по x. Например: 6")
            b = float(input())
            print("Введите e. Например: 0.001")
            eps = float(input())
            print("Хотите увидеть промежуточные рузльтаты поиска экстремума? 1 - да / 0 - нет")
            while True:
                answ = int(input())
                if answ == 1:
                    flag = 1
                    break
                elif answ == 0:
                    flag = 0
                    break
                else:
                    print("Такого ответа нет! Введите корректно.")
            print("Введите кол-во итераций. Например: 10")
            iterations = int(input())
            function = BrentMet()
            function.find(y, a, b, eps, flag, iterations)
        elif userInput == "2.4":
            print("Введите функцию f(x, y). Например:  x**2 - x*y + y**2 + 9*x - 6*y + 20")
            f = input()
            print('Есть ли ограничения по x и y? 1-да / 0 – нет')
            ogr = int(input())
            Xl, Xu, Yl, Yu = -10, 10, -10, 10
            if ogr == 1:
                print("Введите левое ограничение по x. Например: -5")
                Xl = float(input())
                print("Введите правое ограничение по x. Например: 5")
                Xu = float(input())
                print("Введите левое ограничение по y. Например: -5")
                Yl = float(input())
                print("Введите правое ограничение по y. Например: 5")
                Yu = float(input())
            print("Необходимо ввести точку от которой мы будем отталкиваться.")
            print('Введите x. Например: 1')
            x = float(input())
            print('Введите y. Например: 1')
            y = float(input())
            print("Хотите указать e(точность)? 1 - да / 0 - нет")
            ep = int(input())
            e = 10 ** (-5)
            if ep == 1:
                print("Введите e. Например: 0.001")
                e = float(input())
            print("Хотите указать кол-во итераций? 1 - да / 0 - нет")
            it = int(input())
            iter = 500
            if it == 1:
                print("Введите кол-во итераций. Например: 10")
                iter = int(input())
            functions = BFGS()
            functions.find(f, Xl, Xu, Yl, Yu, np.array([[x], [y]]), e, iter)
        elif userInput == "3.1":
            while True:
                print("Какой экстремум вы хотите найти? 1 - максимум \ 0 - минимум")
                q = int(input())
                if q == 1:
                    extr = 1
                    break
                elif q == 0:
                    extr = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")
            print("Введите функцию f(x1, x2, ... , xn). Например: x1**2 + x1*x2**3 + x3**2")
            f = input()
            if extr == 1:
                f = "- (" + f + ")"
                print(f)
            count_param = np.sort(list(set(findall(r'[x]\d', f))))
            print("Введите шаг. Например: 0.01")
            l = float(input())
            print("Введите начальную точку, из которой начинаем спуск.")
            lst_xi = []
            for i in range(len(count_param)):
                print(f'Введите {count_param[i]}. Например: 1')
                xi = [float(input())]
                lst_xi.append(xi)
            while True:
                print("Хотите ввести число итераций? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите кол-во итераций. Например: 500")
                    iter = int(input())
                    break
                elif q == 0:
                    iter = 500
                    break
                else:
                    print("Такой команды нет. Введите снова")
            while True:
                print("Хотите ввести точность оптимизации? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите точность оптимизации. Например: 0.001")
                    e = float(input())
                    break
                elif q == 0:
                    e = 0.0001
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите ввести промежуточные результаты? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag1 = 1
                    break
                elif q == 0:
                    flag1 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите записать промежуточные результаты в датасет? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag2 = 1
                    break
                elif q == 0:
                    flag2 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            function = GradDesentConstStep()
            function.find(f, l, lst_xi, iter, e, flag1, flag2, extr)
        elif userInput == "3.2":
            while True:
                print("Какой экстремум вы хотите найти? 1 - максимум \ 0 - минимум")
                q = int(input())
                if q == 1:
                    extr = 1
                    break
                elif q == 0:
                    extr = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")
            print("Введите функцию f(x1, x2, ... , xn). Например: x1**2 + x1*x2**3 + x3**2")
            f = input()
            if extr == 1:
                f = "- (" + f + ")"
                print(f)
            count_param = np.sort(list(set(findall(r'[x]\d', f))))
            print("Введите шаг. Например: 0.01")
            l = float(input())
            print("Введите начальную точку, из которой начинаем спуск.")
            lst_xi = []
            for i in range(len(count_param)):
                print(f'Введите {count_param[i]}. Например: 1')
                xi = [float(input())]
                lst_xi.append(xi)
            while True:
                print("Хотите ввести число итераций? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите кол-во итераций. Например: 500")
                    iter = int(input())
                    break
                elif q == 0:
                    iter = 500
                    break
                else:
                    print("Такой команды нет. Введите снова")
            while True:
                print("Хотите ввести точность оптимизации? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите точность оптимизации. Например: 0.001")
                    e = float(input())
                    break
                elif q == 0:
                    e = 0.0001
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите вывести промежуточные результаты? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag1 = 1
                    break
                elif q == 0:
                    flag1 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите записать промежуточные результаты в датасет? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag2 = 1
                    break
                elif q == 0:
                    flag2 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите ввести значение параметра оценки? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите значение в интервале (0;1). Например: 0.1")
                    pe = float(input())
                    if 0 < pe < 1:
                        break
                    else:
                        print("Введите корректное значение")
                elif q == 0:
                    pe = 0.1
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите ввести значение параметра дробления? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите значение в интервале (0;1). Например: 0.1")
                    delta = float(input())
                    if 0 < delta < 1:
                        break
                    else:
                        print("Введите корректное значение")
                elif q == 0:
                    delta = 0.95
                    break
                else:
                    print("Такой команды нет. Введите снова")

            function = GradDesentDrobStep()
            function.find(f, l, lst_xi, iter, e, flag1, flag2, extr, pe, delta)
        elif userInput == "3.3":
            while True:
                print("Какой экстремум вы хотите найти? 1 - максимум \ 0 - минимум")
                q = int(input())
                if q == 1:
                    extr = 1
                    break
                elif q == 0:
                    extr = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")
            print("Введите функцию f(x1, x2, ... , xn). Например: x1**2 + x1*x2**3 + x3**2")
            f = input()
            if extr == 1:
                f = "- (" + f + ")"
                print(f)
            count_param = np.sort(list(set(findall(r'[x]\d', f))))
            print("Введите начальную точку, из которой начинаем спуск.")
            lst_xi = []
            for i in range(len(count_param)):
                print(f'Введите {count_param[i]}. Например: 1')
                xi = [float(input())]
                lst_xi.append(xi)
            while True:
                print("Хотите ввести число итераций? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите кол-во итераций. Например: 500")
                    iter = int(input())
                    break
                elif q == 0:
                    iter = 500
                    break
                else:
                    print("Такой команды нет. Введите снова")
            while True:
                print("Хотите ввести точность оптимизации? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите точность оптимизации. Например: 0.001")
                    e = float(input())
                    break
                elif q == 0:
                    e = 0.0001
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите ввести промежуточные результаты? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag1 = 1
                    break
                elif q == 0:
                    flag1 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите записать промежуточные результаты в датасет? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag2 = 1
                    break
                elif q == 0:
                    flag2 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            namegraph = "a"
            if len(lst_xi) == 1:
                print(
                    "У вас функция одной переменной, предлагаем вам увидеть визуализацию функции на 2д графике. Введите название для графика")
                namegraph = input()

            function = FastGradDesent()
            function.find(f, lst_xi, iter, e, flag1, flag2, extr, namegraph)
            if len(lst_xi) == 1:
                print("Гифка с графиком появилась в папке проекта")
        elif userInput == "3.4":
            while True:
                print("Какой экстремум вы хотите найти? 1 - максимум \ 0 - минимум")
                q = int(input())
                if q == 1:
                    extr = 1
                    break
                elif q == 0:
                    extr = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")
            print("Введите функцию f(x1, x2, ... , xn). Например: x1**2 + x1*x2**3 + x3**2")
            f = input()
            if extr == 1:
                f = "- (" + f + ")"
                print(f)
            count_param = np.sort(list(set(findall(r'[x]\d', f))))
            # print("Введите шаг. Например: 0.01")
            # l = float(input())
            print("Введите начальную точку, из которой начинаем спуск.")
            lst_xi = []
            for i in range(len(count_param)):
                print(f'Введите {count_param[i]}. Например: 1')
                xi = float(input())
                lst_xi.append(xi)

            while True:
                print("Хотите ввести точность оптимизации? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    print("Введите точность оптимизации. Например: 0.001")
                    e = float(input())
                    break
                elif q == 0:
                    e = 0.0001
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите ввести промежуточные результаты? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag1 = 1
                    break
                elif q == 0:
                    flag1 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            while True:
                print("Хотите записать промежуточные результаты в датасет? 1 - да / 0 - нет")
                q = int(input())
                if q == 1:
                    flag2 = 1
                    break
                elif q == 0:
                    flag2 = 0
                    break
                else:
                    print("Такой команды нет. Введите снова")

            function = AdjointGrad()
            function.find(f, lst_xi, e, flag1, flag2, extr)
        elif userInput == "4.1":
            y = []
            print("Введите кол-во строк в матрице(n). Например 3")
            n = int(input())
            print("Введите кол-во столбцов в матрице(m). Например 3")
            m = int(input())
            print("Введите массив предсказываемых данных y = (y1, y2, ..., yn)")
            for i in range(n):
                print(f'Введите {i} значение. Например 1')
                y.append(float(input()))
            print("Введите массив предикантов X размерностью n x m")
            X = []
            for i in range(n):
                xij = []
                for j in range(m):
                    print(f'Введите x{i, j}')
                    xij.append(float(input()))
                X.append(xij)

            L = 0.95
            sigma = 0.1
            print("Хотите ввести параметр, отвечающий за вид регуляризации? 1 - да / 0 - нет")
            q = -1
            while q < 0 or q > 1:
                q = int(input())
                if q < 0 or q > 1:
                    print("Неправильный ввод. 1 - да / 0 - нет")

            if q == 1:
                print("Введите L1, или L2, или norm ")
                reg = 'j'
                while reg != "L1" and reg != "L2" and reg != "norm":
                    reg = input()
                    if reg != "L1" and reg != "L2" and reg != "norm":
                        print("Такой комманды нет. Введите снова. L1, или L2, или norm")

                if reg == "L1" or reg == "L2":
                    print(
                        "Введите коэффициент регуляции. Например 0.95. Значение должно быть >=0. (чем больше, тем сильнее регуляризация)")
                    L = -1
                    while L < 0 or L > 1:
                        L = float(input())
                        if L < 0 or L > 1:
                            print("Некорректно введен коэффициент регуляции. Значение должно быть >=0.")

                elif reg == "norm":
                    print(
                        "Введите предполагаемое стандартное отклонение остатков. Например 0.1. Значение должно быть >=0 и <=1. (чем больше, тем слабее регуляризация)")
                    sigma = -1
                    while sigma < 0 or sigma > 1:
                        sigma = float(input())
                        if sigma < 0 or sigma > 1:
                            print(
                                "Некорректно введено предполагаемое стандартное отклонение остатков. Значение должно быть >=0 и <=1.")
            elif q == 0:
                reg = 'None'

            functionss = LinRegr()
            functionss.find(np.array(y).reshape(-1, 1), X, n, m, reg, L, sigma)
        elif userInput == "4.2":
            y = []
            print("Введите кол-во строк в матрице(n). Например 3")
            n = int(input())
            print("Введите кол-во столбцов в матрице(m). Например 3")
            m = int(input())
            print("Введите массив предсказываемых данных y = (y1, y2, ..., yn)")
            for i in range(n):
                print(f'Введите {i} значение. Например 1')
                y.append(float(input()))
            print("Введите массив предикантов X размерностью n x m")
            X = []
            for i in range(n):
                xij = []
                for j in range(m):
                    print(f'Введите x{i, j}')
                    xij.append(float(input()))
                X.append(xij)

            L = 0.95
            sigma = 0.1

            print("Введите степень полинома (целое число больше нуля). Например: 2")
            deg = int(input())
            q = -1

            print("Хотите ввести параметр, отвечающий за вид регуляризации? 1 - да / 0 - нет")
            q = -1
            while q < 0 or q > 1:
                q = int(input())
                if q < 0 or q > 1:
                    print("Неправильный ввод. 1 - да / 0 - нет")

            if q == 1:
                print("Введите L1, или L2, или norm ")
                reg = 'j'
                while reg != "L1" and reg != "L2" and reg != "norm":
                    reg = input()
                    if reg != "L1" and reg != "L2" and reg != "norm":
                        print("Такой комманды нет. Введите снова. L1, или L2, или norm")

                if reg == "L1" or reg == "L2":
                    print(
                        "Введите коэффициент регуляции. Например 0.95. Значение должно быть >=0. (чем больше, тем сильнее регуляризация)")
                    L = -1
                    while L < 0 or L > 1:
                        L = float(input())
                        if L < 0 or L > 1:
                            print("Некорректно введен коэффициент регуляции. Значение должно быть >=0.")

                elif reg == "norm":
                    print(
                        "Введите предполагаемое стандартное отклонение остатков. Например 0.1. Значение должно быть >=0 и <=1. (чем больше, тем слабее регуляризация)")
                    sigma = -1
                    while sigma < 0 or sigma > 1:
                        sigma = float(input())
                        if sigma < 0 or sigma > 1:
                            print(
                                "Некорректно введено предполагаемое стандартное отклонение остатков. Значение должно быть >=0 и <=1.")
            elif q == 0:
                reg = 'None'

            functionss = PolRegres()
            functionss.find(np.array(y).reshape(-1, 1), X, n, m, deg, reg, L, sigma)
        elif userInput == "4.3":
            y = []
            print("Введите кол-во строк в матрице(n). Например 3")
            n = int(input())
            print("Введите кол-во столбцов в матрице(m). Например 3")
            m = int(input())
            print("Введите массив предсказываемых данных y = (y1, y2, ..., yn)")
            for i in range(n):
                print(f'Введите {i} значение. Например 1')
                y.append(math.log1p(float(input())))
            print("Введите массив предикантов X размерностью n x m")
            X = []
            for i in range(n):
                xij = []
                for j in range(m):
                    print(f'Введите x{i, j}')
                    xij.append(float(input()))
                X.append(xij)

            L = 0.95
            sigma = 0.1
            print("Хотите ввести параметр, отвечающий за вид регуляризации? 1 - да / 0 - нет")
            q = -1
            while q < 0 or q > 1:
                q = int(input())
                if q < 0 or q > 1:
                    print("Неправильный ввод. 1 - да / 0 - нет")

            if q == 1:
                print("Введите L1, или L2, или norm ")
                reg = 'j'
                while reg != "L1" and reg != "L2" and reg != "norm":
                    reg = input()
                    if reg != "L1" and reg != "L2" and reg != "norm":
                        print("Такой комманды нет. Введите снова. L1, или L2, или norm")

                if reg == "L1" or reg == "L2":
                    print(
                        "Введите коэффициент регуляции. Например 0.95. Значение должно быть >=0. (чем больше, тем сильнее регуляризация)")
                    L = -1
                    while L < 0 or L > 1:
                        L = float(input())
                        if L < 0 or L > 1:
                            print("Некорректно введен коэффициент регуляции. Значение должно быть >=0.")

                elif reg == "norm":
                    print(
                        "Введите предполагаемое стандартное отклонение остатков. Например 0.1. Значение должно быть >=0 и <=1. (чем больше, тем слабее регуляризация)")
                    sigma = -1
                    while sigma < 0 or sigma > 1:
                        sigma = float(input())
                        if sigma < 0 or sigma > 1:
                            print(
                                "Некорректно введено предполагаемое стандартное отклонение остатков. Значение должно быть >=0 и <=1.")
            elif q == 0:
                reg = 'None'

            functionss = ExpRegres()
            functionss.find(np.array(y).reshape(-1, 1), X, n, m, reg, L, sigma)
        elif userInput == "5.1":
            print("Введите функцию. Например x1**2 + x2**2 + (0.5*1*x1 + 0.5*2*x2)**2 + (0.5*1*x1 + 0.5*2*x2)**4")
            f = str(input())
            f_graph = copy.deepcopy(f)
            print(
                "Введите ограничение (если их несколько то ввести через точку с запятой как в примере). Например x1+x2=0;2*x1-3*x2=0")
            subject_to = str(input())
            # point_min = np.array([0, 0])
            # point_start = np.array([-5, 4.])
            print("Введите координаты начальной точки. Например -5;4")
            point_start = str(input())
            # input_validation
            f = check_expression(f)
            subject_to = check_restr(subject_to, method='Newton')
            point_start = check_point(point_start, f, subject_to, 'Newton')
            # preprocessing
            f, subject_to, point_start = prepare_all(f, subject_to, 'Newton', point_start)
            # solver
            task = Newton(f, subject_to, point_start)
            ans = task.solve()
            # print(np.allclose(ans, point_min))
            print(ans)
            # Рисуем график
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_title('Метод Ньютона')
            ax.set_zlabel('F(x1,x2)')
            ax.set_ylabel('x2')
            ax.set_xlabel('x1')
            x1 = np.linspace(-1, 1, 25)
            x2 = np.linspace(-1, 1, 25)
            x1, x2 = np.meshgrid(x1, x2)
            Z = ne.evaluate(f_graph)
            surf = ax.plot_surface(x1, x2, Z, cmap='viridis', shade=True, alpha=0.5)
            fig.colorbar(surf, shrink=0.5, aspect=10)
            func1 = sp.sympify(f_graph)
            x1, x2 = sp.symbols('x1 x2')
            ax.scatter(float(ans[0]), float(ans[1]),
                       func1.subs([(x1, float(ans[0])), (x2, float(ans[1]))]),
                       c='r', s=50,
                       label=f'Точка экстремума \n x1 = {float(ans[0])},\n x2 = {float(ans[1])},\n'
                             f' F(x1,x2) = {func1.subs([(x1, float(ans[0])), (x2, float(ans[1]))])}')
            ax.legend(labelcolor='black')
            plt.show()
        elif userInput == "5.2":
            print("Введите функцию. Например x1**2 + x2**2 + (0.5*1*x1 + 0.5*2*x2)**2 + (0.5*1*x1 + 0.5*2*x2)**4")
            f = str(input())
            f_graph = copy.deepcopy(f)
            print(
                "Введите ограничение (если их несколько то ввести через точку с запятой как в примере). Например x1+x2<=0;2*x1-3*x2<=1")
            subject_to = str(input())
            # point_min = np.array([0, 0])
            # point_start = np.array([-5, 4.])
            print("Введите координаты начальной точки. Например -5;4")
            point_start = str(input())

            # input_validation
            f = check_expression(f)
            subject_to = check_restr(subject_to, method='log_barrier')
            point_start = check_point(point_start, f, subject_to, 'log_barrier')
            # preprocessing
            f, subject_to, point_start = prepare_all(f, subject_to, 'log_barrier', point_start)
            # solver
            task = LogBarrirers(f, subject_to, point_start)
            ans = task.solve()
            # print(np.allclose(ans, point_min))
            print(ans)

            # Рисуем график
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_title('Метод логарифмических барьеров ')
            ax.set_zlabel('F(x1,x2)')
            ax.set_ylabel('x2')
            ax.set_xlabel('x1')

            x1 = np.linspace(-1, 1, 25)
            x2 = np.linspace(-1, 1, 25)
            x1, x2 = np.meshgrid(x1, x2)
            Z = ne.evaluate(f_graph)

            surf = ax.plot_surface(x1, x2, Z, cmap='viridis', shade=True, alpha=0.5)
            fig.colorbar(surf, shrink=0.5, aspect=10)

            func1 = sp.sympify(f_graph)

            x1, x2 = sp.symbols('x1 x2')

            ax.scatter(float(ans[0]), float(ans[1]),
                       func1.subs([(x1, float(ans[0])), (x2, float(ans[1]))]),
                       c='r', s=50,
                       label=f'Точка экстремума \n x1 = {float(ans[0])},\n x2 = {float(ans[1])},\n'
                             f' F(x1,x2) = {func1.subs([(x1, float(ans[0])), (x2, float(ans[1]))])}')

            ax.legend(labelcolor='black')
            plt.show()
        elif userInput == "5.3":
            print("Введите функцию. Например x1**2 + x2**2 + (0.5*1*x1 + 0.5*2*x2)**2 + (0.5*1*x1 + 0.5*2*x2)**4")
            f = str(input())
            f_graph = copy.deepcopy(f)
            print(
                "Введите ограничение (если их несколько то ввести через точку с запятой как в примере). Например x1+x2<=0;2*x1-3*x2<=1")
            subject_to = str(input())
            # point_min = np.array([0, 0])
            # point_start = np.array([-5, 4.])
            print("Введите координаты начальной точки. Например -5;4")
            point_start = str(input())

            # input_validation
            f = check_expression(f)
            subject_to = check_restr(subject_to, method='primal-dual')
            point_start = check_point(point_start, f, subject_to, 'primal-dual')
            # preprocessing
            f, subject_to, point_start = prepare_all(f, subject_to, 'primal-dual', point_start)
            # solver
            task = PrimalDual(f, subject_to, point_start)
            ans = task.solve()
            print(ans[0])

            # Рисуем график
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_title('Прямо-двойственный метод внутренней точки')
            ax.set_zlabel('F(x1,x2)')
            ax.set_ylabel('x2')
            ax.set_xlabel('x1')

            x1 = np.linspace(-1, 1, 25)
            x2 = np.linspace(-1, 1, 25)
            x1, x2 = np.meshgrid(x1, x2)
            Z = ne.evaluate(f_graph)

            surf = ax.plot_surface(x1, x2, Z, cmap='viridis', shade=True, alpha=0.5)
            fig.colorbar(surf, shrink=0.5, aspect=10)

            func1 = sp.sympify(f_graph)

            x1, x2 = sp.symbols('x1 x2')

            ax.scatter(float(ans[0][0]), float(ans[0][1]),
                       func1.subs([(x1, float(ans[0][0])), (x2, float(ans[0][1]))]),
                       c='r', s=50,
                       label=f'Точка экстремума \n x1 = {float(ans[0][0])},\n x2 = {float(ans[0][1])},\n'
                             f' F(x1,x2) = {func1.subs([(x1, float(ans[0][0])), (x2, float(ans[0][1]))])}')

            ax.legend(labelcolor='black')
            plt.show()
        elif userInput == "6.1":
            print("Мы будем составлять массив предсказываемых значений и массив обучающей выборки с помощью функции"
                  "make_classification. Для этого нужно ввести ее параметры. Пример параметров: "
                  "make_classification(n_samples = 1000, n_features = 4, class_sep = 0.5, random_state = 0) ")
            print("Введите параметр n_samples. Например: 1000")
            n_samp = int(input())
            print("Введите параметр n_features. Например: 4")
            n_feat = int(input())
            print("Введите параметр class_sep. Например: 0.5")
            class_s = float(input())
            print("Введите параметр random_state. Например: 0")
            random_s = int(input())

            x1, y1 = make_classification(n_samples=n_samp, n_features=n_feat, class_sep=class_s, random_state=random_s)

            Сlassification.logistic(x1, y1)
        elif userInput == "6.2":
            print("Мы будем составлять массив предсказываемых значений и массив обучающей выборки с помощью функции"
                  "make_classification. Для этого нужно ввести ее параметры. Пример параметров: "
                  "make_classification(n_samples = 1000, n_features = 4, class_sep = 0.5, random_state = 0) ")
            print("Введите параметр n_samples. Например: 1000")
            n_samp = int(input())
            print("Введите параметр n_features. Например: 4")
            n_feat = int(input())
            print("Введите параметр class_sep. Например: 0.5")
            class_s = float(input())
            print("Введите параметр random_state. Например: 0")
            random_s = int(input())

            x1, y1 = make_classification(n_samples=n_samp, n_features=n_feat, class_sep=class_s, random_state=random_s)

            Сlassification.logistic_rbf(x1, y1)
        elif userInput == "6.3":
            print("Мы будем составлять массив предсказываемых значений и массив обучающей выборки с помощью функции"
                  "make_classification. Для этого нужно ввести ее параметры. Пример параметров: "
                  "make_classification(n_samples = 1000, n_features = 4, class_sep = 0.5, random_state = 0) ")
            print("Введите параметр n_samples. Например: 1000")
            n_samp = int(input())
            print("Введите параметр n_features. Например: 4")
            n_feat = int(input())
            print("Введите параметр class_sep. Например: 0.5")
            class_s = float(input())
            print("Введите параметр random_state. Например: 0")
            random_s = int(input())

            x1, y1 = make_classification(n_samples=n_samp, n_features=n_feat, class_sep=class_s, random_state=random_s)

            Сlassification.logistic_rbf(x1, y1)
        elif userInput == "6.4":
            print("Эта функция запускается на автоматически генерируемых данных")

            x = Сlassification.funcForInput()
            print("Сгенерироавнные данные: ")
            print(x)
            Сlassification.opornieVectora(x)
        elif userInput == "7.1":
            print(1)
        elif userInput == "7.2":
            print(1)
        elif userInput == "8.1":
            print(1)
        elif userInput == "8.2":
            print(1)
        elif userInput == "8.3":
            print(1)
        elif userInput == "8.4":
            print(1)
        else:
            print("Извините, такой метод не найден.")
