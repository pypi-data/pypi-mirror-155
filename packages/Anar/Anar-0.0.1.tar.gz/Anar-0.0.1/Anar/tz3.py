import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp

class bc:

    def gradient_descent_fixed(w_init, obj_func, grad_func, learning_rate=0.05,
                               max_iterations=500, threshold=1e-2):
        w = w_init
        w_history = w
        f_history = obj_func(w)
        delta_w = np.zeros(w.shape)
        i = 0
        diff = 1.0e10

        while i < max_iterations and diff > threshold:
            delta_w = -learning_rate * grad_func(w)
            w = w + delta_w

            # store the history of w and f
            w_history = np.vstack((w_history, w))
            f_history = np.vstack((f_history, obj_func(w)))

            # update iteration number and diff between successive values
            # of objective function
            i += 1
            diff = np.absolute(f_history[-1] - f_history[-2])
            print(f'X = {w_history[-1]}', f'Y = {f_history[-1]}', f'Iter = {i}', sep='\n')
            print({'Значение': f_history[-1], 'Кол-во итераций': i})
        return w_history, f_history

    w_hist, f_hist = gradient_descent_fixed(w_init = np.array([1, 1]), obj_func=f, grad_func=gradient_f,
                                            learning_rate=0.05)

    print(f'X = {w_hist[-1]}', f'Y = {f_hist[-1]}', sep='\n')

    x = np.linspace(-1, 1, 1000)
    y = np.linspace(-1, 1, 1000)
    X, Y = np.meshgrid(x, y)
    Z = f([X, Y])

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap='jet')

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111)
    ax.contour(X, Y, Z, levels=50)

    ax.plot(w_hist[:, 0], w_hist[:, 1])

x1, y1 = sp.symbols('x1 y1')
func = 0.26 * (x1 ** 2 + y1 ** 2) - 0.48 * x1 * y1
sp.derive_by_array(func, [x1, y1])

bc.gradient_descent_fixed(func)