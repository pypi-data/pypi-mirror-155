from .brent import *
from sympy import *
import numpy as np
from re import findall
from re import sub


class AdjGrad:
    def find(self, z, x, e, flag1, flag2, extr):
        c = 0
        func = sympify(z)
        l = Symbol('l')
        lst_xi = np.sort(list(set(findall(r'[x]\d', z))))

        grad = []
        for i in range(len(lst_xi)):
            grad.append(func.diff(lst_xi[i]))
        x = np.array(x)
        j = 0
        while True:
            i = 0
            su = dict(zip(lst_xi, x))
            calc_grad = []
            for k in range(len(lst_xi)):
                calc_grad.append(grad[k].subs(su))
            calc_grad = np.array(calc_grad)
            S = -1 * calc_grad
            x_jk = x

            while i + 1 < len(lst_xi):

                lam = x + l * S
                su1 = dict(zip(lst_xi, lam))
                f_l = str(func.subs(su1))
                f_l = sub(r'l', r'x', f_l)
                lam = BrentMet()

                l_min = lam.find(f_l, -100, 100, e * 10, 100)
                # minimize(lambdify('x', sympify(f_l)), [0])['x'][0]

                x_jk_1 = x_jk + l_min * S

                su_xjk_1 = dict(zip(lst_xi, x_jk_1))
                calc_grad_xjk_1 = []
                for k in range(len(lst_xi)):
                    calc_grad_xjk_1.append(grad[k].subs(su_xjk_1))
                calc_grad_xjk_1 = np.array(calc_grad_xjk_1)

                sum_grad = (calc_grad ** 2).sum()
                sum_grad_k = (calc_grad_xjk_1 ** 2).sum()
                Skj = -1 * calc_grad_xjk_1 + (sum_grad_k / sum_grad) * S

                met_Skj = (Skj ** 2).sum() ** (1 / 2)
                #su_after = su_xjk_1

                x_beauty = x_jk_1
                if flag1 == 1:
                    print(tuple(x_beauty))

                x_met = ((x_jk_1 - x_jk) ** 2).sum() ** (1 / 2)
                # Написать датасеты использовать x_beauty
                if extr == 0:

                    if (met_Skj < e) or (x_met < e):
                        #print(f'Минимум в точке {tuple(x_beauty)}')
                        #print(f'Значение функции в точке минимума {float(func.subs(su_after))}')
                        c = 1
                        break
                else:
                    if (met_Skj < e) or (x_met < e):
                        #print(f'Максимум в точке {tuple(x_beauty)}')
                        #print(f'Значение функции в точке максимума {float(func.subs(su_after))}')
                        c = 1
                        break
                x_jk = x_jk_1
                S = Skj
                i += 1
            if c == 1:
                break
            x = x_jk
            j += 1
        return x_beauty

#function = AdjGrad()
#function.find('0.95*x1 + 0.95*x2 + 0.5*(-1.0*x1 + 1.0*x2 + 1)**2', [0, 0], 0.0001, 0, 0, 0)
