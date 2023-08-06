import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as LA
from sympy import *

class SGD:
    def f(x, y):
        return -np.cos(x) * np.cos(y) * np.exp(-((x - np.pi) ** 2 + (y - np.pi) ** 2))

    def SGD_grad(X, Y):
        x, y = symbols('x y')
        eq = -cos(x) * cos(y) * exp(-((x - pi) ** 2 + (y - pi) ** 2))
        v = list(ordered(eq.free_symbols))
        gradient = lambda f, v: Matrix([f]).jacobian(v)
        subs_grad = gradient(eq, v).subs([(x, X), (y, Y)]).evalf()
        return np.array(subs_grad).astype(np.float64)[0]

    def stochastic_gradient_descent(max_epochs, xy_start, obj_func = f, grad_func = SGD_grad):
        xy = xy_start
        xy_history = xy_start
        f_history = obj_func(*xy_start)
        delta_xy = np.zeros(xy_start.shape)
        i = 0
        diff = 1
        l_rate = 0.01
        while i < max_epochs and diff > 1e-8:
            choose_var = np.random.randint(xy_start.shape[0])
            grad = np.zeros(shape=xy_start.shape[0])
            grad[choose_var] = grad_func(*xy)[choose_var]
            delta_xy = -l_rate * np.array(grad) + 0.6 * delta_xy
            xy = xy + delta_xy

            i += 1
            xy_history = np.vstack((xy_history, xy))
            f_history = np.vstack((f_history, obj_func(*xy)))
            diff = np.absolute(f_history[-1] - f_history[-2])
        return xy_history, f_history

    def SGD_visualize(opt_res):
        x = np.linspace(1, 5, 2000)
        y = np.linspace(1, 5, 2000)
        X, Y = np.meshgrid(x, y)
        Z = SGD.f(X, Y)
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', shade=True, alpha=0.5)
        ax.scatter(opt_res[-1], opt_res[-1], -1, facecolor='red', s=55)
        fig.colorbar(surf, shrink=0.5, aspect=10)
        plt.show()


#opt_res,f_opt = SGD.stochastic_gradient_descent(max_epochs = 500,xy_start = np.array([2.5, 2.5]))
#print(opt_res[-1])
#SGD.SGD_visualize(opt_res)