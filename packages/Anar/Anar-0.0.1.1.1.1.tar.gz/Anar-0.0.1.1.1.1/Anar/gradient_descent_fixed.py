def gradient_descent_fixed(w_init, obj_func, grad_func, learning_rate=0.05,
                           max_iterations=500, threshold=1e-2):
    """
    Функция поиска минимума целевой функции одной переменной методом градиентного спуска, который находит оптимальное решение, делая шаг в сторону максимальной скорости уменьшения функции.
    :param obj_fun: objective function that is going to be minimized (call val,grad = obj_fun(w)).
    :param w_init: starting point Mx1
    :param grad_func: gradiation function that is going to be minimized (call val,grad = obj_fun(w)).
    :param max_iterations: number of epochs / iterations of an algorithm
    :param learning_rate: learning rate
    :return: function optimizes obj_fun using gradient descent. It returns (w,func_values),
    where w is optimal value of w and func_valus is vector of values of objective function [epochs x 1] calculated for each epoch
        """

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