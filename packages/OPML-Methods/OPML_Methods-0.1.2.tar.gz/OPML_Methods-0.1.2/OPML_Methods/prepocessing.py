import numpy as np
import re
import math

from math import sqrt
from math import isclose

import sympy.integrals.rubi.utility_function
from sympy import sympify, Symbol, simplify
from sympy.utilities.lambdify import lambdastr
from typing import Optional, Callable
import autograd.numpy as npa


# preprocessing
def prepare_all(function: str, restriction: str, method: str, started_point: Optional[str] = None) -> tuple:
    """
    Функция подготавливает входные данные. В случае некорректного формата или математически неправильных записей будет
    вызвана ошибка.

    Parameters
    ------------
    function: str
        Функция для оптимизации. Функция в аналитическом виде, записанная в виде строки.

    restriction: str
        Строка ограничений, разделенными точкой с запятой. Ограничения записываются в том же виде,
        что и функция: функция в аналитическом виде в строке.(ограничения вида (=, =>, <=).

    started_point: str
        Координаты стартовой точки. Должна быть внутренней!

    method: str
        Метод для решения задачи. В зависимости от него будут переписываться ограничения для задачи. Принимает одно из
        значений среди ['None', 'primal_dual', ...]

    Returns
    -------
    func: Callable
        Функция, представленная в виде питоновской функции.
    restr: list
        Список питоновских функций, которые представляют собой функции ограничений.
    point: np.ndarray
        Массив с координатами точки.
    """

    func = sympify(function)
    func = to_callable(func)
    restriction = restriction.split(';')
    restr = []
    if method == 'Newton':
        for i in restriction:
            left, right = i.split('=')
            left = left.strip()
            right = right.strip()
            left, right = sympify(left), sympify(right)
            left -= right
            left = to_callable(left)
            restr.append(left)
    if method == 'primal-dual':
        for i in restriction:
            if i.find('>=') != -1:
                spliter = '>='
            elif i.find('<=') != -1:
                spliter = '<='
            left, right = i.split(spliter)
            left = left.strip()
            right = right.strip()
            left, right = sympify(left), sympify(right)
            left -= right
            left = to_callable(left)
            restr.append(left)
    if method == 'log_barrier':
        for i in restriction:
            if i.find('>=') != -1:
                spliter = '>='
            elif i.find('<=') != -1:
                spliter = '<='
            left, right = i.split(spliter)
            left = left.strip()
            right = right.strip()
            left, right = sympify(left), sympify(right)
            left -= right
            left = to_callable(left)
            restr.append(left)
            # print(i)
    coords = started_point.split(';')
    point = []
    for i in range(len(coords)):
        point.append(float(coords[i].strip()))
    point = np.array(point)
    return func, restr, point


def to_callable(expression: sympy.core) -> Callable:
    """
    Преобразует исходное выражение в функцию питона.

    Parameters
    ------------
    expression: sympy expression
        Преобразует выражение sympy в питоновскую функцию от массива.

    Returns
    -------
    func: Callable
        Питоновская функция от массива.
    """

    str_vars = [str(i) for i in expression.free_symbols]
    str_vars = sorted(str_vars, key=lambda x: int(x[1:]), reverse=True)
    dict_for_vars = {i: f'x[{int(i[1:]) - 1}]' for i in str_vars}
    func = lambdastr(['x'], expression)
    for i in str_vars:
        i = str(i)
        func = func.replace(i, dict_for_vars[i])
    # #print(func[9:])
    func = 'f=' + func
    d = {}
    exec(func, {'math': npa}, d)
    func = d['f'] # готовая функция
    return func


def make_matrix(expressions: list, xs: set) -> tuple:
    """
    Функция преобразует линейные sympy выражения в матрицы.

    Parameters
    ----------
    expressions: list
        Список ограничений фунции (в виде списка строк).
    xs: set
        Множество переменных в задаче.

    Returns
    -------
    A: np.ndarray
        Матрица весов при x.
    b: np.ndarray
        Вектор весов справа.
    """

    A = []
    b = []
    for i in expressions:
        l, r = i.split('=')
        b.append(float(r))
        exp = sympify(l)
        d = dict(zip(xs, [0] * len(xs)))
        coefs = [0]*len(xs)
        for j in exp.free_symbols:
            d[j] = 1
            coefs[int(str(j)[1:]) - 1] = float(exp.subs(d))
            d[j] = 0
        A.append(coefs)
    A = np.array(A)
    b = np.array(b)
    return A, b



if __name__ == '__main__':
    f, restr, p = prepare_all('x1**2 - x3', 'x2 - x4 = 3', 'Newton', '0;0;0;0')
    # print(restr[0]([1, 3, 2, 0]))