import re

from typing import Optional
from sympy.parsing.sympy_parser import parse_expr
from sympy import sympify, exp, Symbol

ALLOWED_OPERATIONS = ['log', 'ln', 'factorial', 'sin', 'cos', 'tan', 'cot', 'pi', 'exp', 'sqrt', 'root', 'abs']


def check_expression(expression: str) -> str:
    """
    Функция для проверки выражения на корректность. Принимает на вход строку с функцией
    в аналитическом виде, возвращает строку. Функция обязательно должна быть
    только от аргументов вида x1, x2, ..., xn.

    Parameters:
    ------------
    expression: str
        Строка содержащая функцию для проверки.

    Returns:
    -------
    str: str
        Функция в виде строки.
    """

    expression = expression.strip()
    if expression.find('—') != -1:
        expression = expression.replace('—', '-')

    if expression.find('–') != -1:
        expression = expression.replace('–', '-')

    checker = compile(expression, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
    var_checker = re.compile(r'^x{1}[0-9]+$')

    for name in checker.co_names:
        if name not in ALLOWED_OPERATIONS:
            if not (var_checker.match(name) and name != 'x0'):
                raise NameError(f"The use of '{name}' is not allowed")

    function = sympify(expression, {'e': exp(1)}, convert_xor=True)
    return str(function)


def check_restr(restr_str: str, method: str, splitter: Optional[str] = ';') -> str:
    """
    Проверяет корректность и читаемость ограничений.

    Parameters
    ----------
    restr_str: str
        Строка с ограничениями в аналитическом виде.

    method: str
        Название метода для решения задачи.

    splitter: Optional[str] = ';'
        Строка-разделитель, которым разделены градиенты.

    Returns
    -------
    restrs: str
        Строка с ограничениями в аналитическом виде, разделенные ';'.
    """

    g = restr_str.split(splitter)

    ans = []
    for i in range(len(g)):
        if method == 'Newton':
            if g[i].find('<=') != -1 or g[i].find('>=') != -1:
                raise ValueError(f'Для метода {method} ограничения должны быть равенствами.')
            else:
                if g[i].count('=') != 1:
                    raise ValueError(f'Неправильно задано ограничение {g[i]}')
                left, right = g[i].split('=')
                left, right = sympify(check_expression(left)), sympify(check_expression(right))
                left = left - right
                right = right - right

            checked = str(left) + '=' + str(right)
            ans.append(checked)
        if method == 'primal-dual':
            if g[i].count('=') > 1:
                raise ValueError(f'Неправильно задано ограничение {g[i]}')
            if g[i].find('>=') != -1:
                splitt = '>='
            elif g[i].find('<=') != -1:
                splitt = '<='
            else:
                raise ValueError(f'Неправильно задано ограничение {g[i]}')
            left, right = g[i].split(splitt)
            left, right = sympify(check_expression(left)), sympify(check_expression(right))
            if splitt == '>=':
                left -= right
            if splitt == '<=':
                left = -left
                right = -right
                left -= right
            right -= right
            checked = str(left) + '>=' + str(right)
            ans.append(checked)
        if method == 'log_barrier':
            if g[i].find('<=') != -1 or g[i].find('>=') != -1:
                if g[i].count('=') > 1:
                    raise ValueError(f'Неправильно задано ограничение {g[i]}')
                if g[i].find('>=') != -1:
                    splitt = '>='
                elif g[i].find('<=') != -1:
                    splitt = '<='
                left, right = g[i].split(splitt)
                left, right = sympify(check_expression(left)), sympify(check_expression(right))
                if splitt == '>=':
                    left -= right
                if splitt == '<=':
                    left = -left
                    right = -right
                    left -= right
                right -= right
                checked = str(left) + '>=' + str(right)
                ans.append(checked)
            else:
                raise ValueError(f'''Для метода {method} ограничения типа равенств пока
                 не поддерживаются, можем добавить.''')
                # if g[i].count('=') != 1:
                #     raise ValueError(f'Неправильно задано ограничение {g[i]}')

    # print(ans)
    restrs = ";".join(ans)
    return restrs


def check_float(value: str) -> float:
    """
    Проверяет введеное значение на корректность и на наличие инъекций, а затем
    конвертирует в float, если это возможно. Поддерживает операции с pi и e.
    Parameters:
    ------------
    values: str
        строка в которой содержится выражение
    Returns:
    -------
    float
        значение переведенное из строки в float
    """
    value = value.strip()
    if value.find('^') != -1:
        value = value.replace('^', '**')
    checker = compile(value, '<string>', 'eval')  # Может выдать SyntaxError, если выражение некорректно
    for name in checker.co_names:
        if name not in ['pi', 'e', 'exp']:
            raise ValueError(f'Нельзя использовать имя {name}')
    value = float(parse_expr(value, {'e': exp(1)}))
    return value


def check_point(point_str: str, function: str, restrs: str, method: str, splitter: Optional[str] = ';') -> str:
    """
    Функция проверяет корректность введеной точки x0.

    Parameters
    ----------
    point_str: str
         Координаты точки в виде строки. Если строка пустая или 'None', то будет применяться метод первой фазы.

    function: str
        Функция минимизации. Нужна для проверки корректности точки и размерностей.

    restrs: str
        Строка ограничений. Нужна для проверки размерности точки и для проверки точки на внутренность.

    method: str
        Название метода для решения задачи.

    splitter: Optional[str] = ';'
        Разделитель, которым разделены координаты в строке.

    Returns
    -------
     point: str
        Строка с координатами точки, разделенные знаком ';'.
    """

    if point_str == '' or point_str == 'None':
        return ''
    coords = point_str.split(splitter)
    for i in range(len(coords)):
        coords[i] = str(check_float(coords[i]))
    f = sympify(function)
    if method == 'Newton':
        r = [sympify(i.split('=')[0]) for i in restrs.split(';')]
    elif method == 'primal-dual':
        r = [sympify(i.split('>=')[0]) if i.find('>=') != -1 else sympify(i.split('<=')[0]) for i in restrs.split(';')]
    elif method == 'log_barrier':
        r = [sympify(i.split('>=')[0]) if i.find('>=') != -1 else sympify(i.split('<=')[0]) for i in restrs.split(';')]

    max_ind = 0
    for i in [f]+r:
        i = max([int(str(j)[1:]) for j in i.free_symbols])
        max_ind = max(max_ind, i)
    if max_ind != len(coords):
        raise ValueError('Размерность точки не сходится с размерностями функций из задачи')
    d = {f'x{i+1}': float(coords[i]) for i in range(len(coords))}

    if method == 'primal-dual':
        for i in r:
            # print(i.subs(d), i)
            if float(i.subs(d)) <= 0:
                raise ValueError('Точка не внутренняя')
    if method == 'log_barrier':
        for i in r:
            # print(i.subs(d), i)
            if float(i.subs(d)) <= 0:
                raise ValueError('Точка не внутренняя')
    points = ';'.join(coords)
    return points


if __name__ == '__main__':
    func = 'x1**2 - x3'
    restr = 'x2 - x4 >= 3'
    meth = 'log_barrier'
    start = '0;4;0;0'

    # костяк проверок
    s = check_expression(func)
    # # print(s)
    r = check_restr(restr, method=meth)
    # # print(r)
    #
    p = check_point(start, s, r, meth)
    # # print(p)
