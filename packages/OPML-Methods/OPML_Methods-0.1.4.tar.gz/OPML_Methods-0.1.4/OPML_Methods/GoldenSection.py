from sympy import *


class GoldenSection:
    def find(self, y, Xl, Xu, e, ea, flag, iter):
        """
        Функция находит экстремум функции одной переменной методом золотого сечения.
        Parameters
        ===========
        :param y: str
            строковая функция f(x)
        :param Xl: float
            интервал "от" по х
        :param Xu: float
            интервал "до" по х
        :param e: float
            эпсилон - точность исследования
        :param ea: float
            начальная точность (потом пеерсчитывается)
        :param flag: int
            если 1 то промежуточные расчеты выводятся если 0 то нет
        :param iter: int
            количество итерация
        Returns
        ===========
        экстремум функции, если flag=1, выводятся промежуточные значения
        """
        func = sympify(y)
        x = Symbol('x')

        R = (5 ** 0.5 - 1) / 2

        D = R * (Xu - Xl)
        x1 = Xl + D
        x2 = Xu - D
        f1 = func.subs(x, x1)
        f2 = func.subs(x, x2)

        if flag == 'True':
            print(' xopt')

        i = 1
        # Golden-Section Search Method
        while (ea > e) and (i <= iter):
            if f1 < f2:
                Xl = x2
                x2 = x1
                f2 = f1
                x1 = Xl + R * (Xu - Xl)
                f1 = func.subs(x, x1)

            else:
                Xu = x1
                x1 = x2
                f1 = f2
                x2 = Xu - R * (Xu - Xl)
                f2 = func.subs(x, x2)

            if f1 < f2:
                xopt = x1
            else:
                xopt = x2

            ea = (1 - R) * abs((Xu - Xl) / xopt) * 100
            if flag == 'True':
                print(f"{xopt:>10.7f}")
            i += 1

        self.x_min = xopt
        self.y_min = func.subs(x, xopt)
        return (self.x_min, self.y_min)

# function = GoldenSection()
##function.find('4 - x ** 2 - 0.2 * x ** 3', Xl, Xu, e, ea, flag, iter)
##function.find('-5*x**5 + 4*x**4 - 12* x**3 + 11*x**2 - 2*x - 1', -0.5, 0.5, e, ea, flag, iter)
##function.find('(log(x-2))**2 + (log(10-x))**2 - x**0.2', 6, 9.9, e, ea, flag, iter)
##function.find('-3*x*sin(0.75*x) + exp(-2*x)', 0, 2*3.14, e, ea, flag, iter)
##function.find('exp(3*x) + 5* exp(-2*x)', 0, 1, e, ea, flag, iter)
##function.find('0.2*x*log(x) + (x - 2.3)**2', 0.5, 2.5, e, ea, flag, iter)
##function.find('10 + (x**2 - 10*cos(2*3.14*x))', -5.12, 5.12, e, ea, flag, iter)
##function.find('x**2', -5, 5, e, ea, flag, iter)
##function.find('-x*sin((abs(x))**(1/2))', -500, 500, e, ea, flag, iter)
#
# print(function.x_min)
