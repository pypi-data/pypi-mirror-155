import numpy as np
from typing import Callable, Optional
from math import isclose
import autograd.numpy as npa
from autograd import grad, hessian
from numpy.linalg import norm
from matplotlib import pyplot as plt
import numexpr as ne
import sympy as sp
import copy


from .input_validation import check_expression, check_restr, check_point
from .prepocessing import prepare_all


class PrimalDual:
    """
    Метод решения задачи Прямо-двойственным методом внутренней точки.

    Parameters
    ----------
    function: Callable
        Функция для минимизации.

    restrictions: list
        Список функций (в смысле питоновских функций), которые представляют собой ограничения типа '>='.

    x0: np.ndarray
        Плоский массив, содержащий начальную точку.

    k: Optional[float] = 0.9
        Коэфициент для уменьшения mu на каждом шаге. 0 < k < 1.

    eps: Optional[float] = 1e-12
        Точность. От этого параметра зависит, когда будет остановлен итерационные процесс поиска решения. При
        слишком малых значениях, есть вероятность бесконечного цикла или nan в ответе.
    """

    def __init__(self,
                 function: Callable,
                 restrictions: list,
                 x0: np.ndarray,
                 k: Optional[float] = 0.9,
                 eps: Optional[float] = 1e-12):
        self.function = function
        self.restrictions = restrictions
        self.k = k
        self.x = x0
        self.lam = np.array([0.5 for i in range(len(restrictions))])
        self.eps = eps

        self.grad_g = [grad(i) for i in self.restrictions] # список из функций, которые вычисют градиент ограничений
        self.grad_f = grad(self.function) # функция вычисялет градиент функции оптимизации

        self.mu = 1
        self.N_con = len(restrictions)

    def solve(self):
        """
        Метод решает задачу.

        Returns
        -------
        x: np.ndarray
            Массив с решениями прямой задачи.

        lam: np.ndarray
            Массив с решениями двойственной задачи.
        """

        A = np.vstack([self.grad_g[i](self.x) for i in range(self.N_con)])
        C = np.diag([i(self.x) for i in self.restrictions])
        w = hessian(self.minimize_func)
        while not isclose(norm(C@self.lam), 0, abs_tol=self.eps):
            A = np.vstack([self.grad_g[i](self.x) for i in range(self.N_con)])
            W = w(self.x)
            C = np.diag([i(self.x) for i in self.restrictions])
            matr = np.vstack((np.hstack((W, -A.T)), np.hstack((np.diag(self.lam) @ A, C))))
            top = (-self.minimize_func_grad() + A.T @ self.lam).reshape(-1, 1)
            bot = (self.mu - C @ self.lam).reshape(-1, 1)
            vec = np.vstack((top, bot))
            new = np.linalg.solve(matr, vec)
            new_x = new.flatten()[:-self.N_con]
            new_lam = new.flatten()[-self.N_con:]
            # поиск длины шага
            alpha = 1
            # calc_con = lambda x: np.array([i(x) for i in con])
            while (self.calc_constrains(self.x + alpha * new_x) < 0).any() or ((self.lam + alpha * new_lam) < 0).any():
                alpha /= 2
            self.x = self.x + alpha * new_x
            self.lam = self.lam + alpha * new_lam
            self.mu = 0.9 * self.mu
        return self.x, self.lam

    def calc_constrains(self, x):
        """
        Метод подставляет x в функции ограничения.

        Parameters
        ----------
        x: np.ndarray
            Значения точки для подстановки в ограничения.

        Returns
        -------
        ans: np.ndarray
            Массив со значениями функций ограничений.
        """
        ans = np.array([self.restrictions[i](x) for i in range(self.N_con)])
        return ans

    def minimize_func(self, x):
        """
        Метод вычисляет значения функци вместе с барьерной функцией (Лагранжиан).

        Returns
        -------
        r: float
            Значения указанной в описании функции.
        """
        r = self.function(x)
        for i in self.restrictions:
            r -= self.mu*npa.log(i(x))
        return r

    def minimize_func_grad(self):
        """
        Метод вычисляет значения градиента Лагранжиана.

        Returns
        -------
        g : float
            Значения указанной в описании функции.
        """
        g = self.grad_f(self.x)
        grads = [i(self.x) for i in self.grad_g]
        for i in range(self.N_con):
            g -= self.mu*grads[i]
        return g


if __name__ == "__main__":
    #  первый пример, точка (0, 1)
    # f = 'x1 - 2*x2'
    # subject_to = ['1 + x1 - x2**2 >= 0', 'x2>=0']
    # start_point = np.array([0.5, 0.5])
    # right_point = (0, 1)
    # vars = get_variables(f)
    # второй пример, точка (1.5, 1.5)
    # f = '2*x1 + 2*x2'
    # subject_to = ['x1 + x2 >= 3', 'x1>=0', 'x2>=0']
    # right_point = (1.5, 1.5)
    # start_point = np.array([0.5, 0.5])
    # vars = get_variables(f)
    # третий пример, точка (1.5, 1.5)
    # f = '3*x1 + 5*x2'
    # subject_to = ['x1 <= 3', '2*x2<=12', '3*x1+2*x2<=18', 'x1>=0', 'x2>=0']
    # right_point = (2, 6)
    # start_point = np.array([2, 6.])
    # vars = get_variables(f)
    # правильный пример (zakharov)
    # def f(x):
    #     return x[0] ** 2 + x[1] ** 2 + (0.5 * 1 * x[0] + 0.5 * 2 * x[1]) ** 2 + (0.5 * 1 * x[0] + 0.5 * 2 * x[1]) ** 4

    f = 'x1**2 + x2**2 + (0.5*1*x1 + 0.5*2*x2)**2 + (0.5*1*x1 + 0.5*2*x2)**4'
    f_graph = copy.deepcopy(f)
    subject_to = 'x1+x2<=0;2*x1-3*x2<=1'
    # point_min = [0, 0]
    # point_start = np.array([-5, 4.])
    point_start = '-5;4'

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

