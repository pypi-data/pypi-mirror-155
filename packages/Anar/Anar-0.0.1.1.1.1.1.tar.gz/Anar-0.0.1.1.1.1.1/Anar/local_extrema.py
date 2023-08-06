import numpy as np
import sympy as sm
import pandas as pd

def local_extrema(variab, func, restr):
    """
    Функцция поиска локальных экстремумов функции двух переменных
    :param variab: кортеж состоящий из переменных, которые являются sympy symbols
    :param func: sympy expression
    :param restr: возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :return: Список координат и значение функции в точке, для всех точек локальных экстремумов,
     с указанием типа экстремума (минимум, максимум, седловая точка)
    """
    x, y = sm.symbols('x, y')  # !!! комплексные переменные

    func = func.subs({variab[0]: x, variab[1]: y})  # заменяем переменные во избежание комплексных ответов
    variab1_d = sm.diff(func, x)  # дифференцируем по каждой из переменных
    variab2_d = sm.diff(func, y)

    sol = sm.solve([variab1_d,
                    variab2_d],
                   [x, y], dict=True)  # приравниваем частные производные к нулю и решаем систему

    sol_restr_all = []  # !!!
    sol_restr = []
    for solution in sol:
        if solution[x].is_real and solution[y].is_real:
            if restr[variab[0]][0] <= solution[x] <= restr[variab[0]][1] and \
                    restr[variab[1]][0] <= solution[y] <= restr[variab[1]][1]:
                sol_restr.append(solution)
                sol_restr_all.append(solution)

        else:

            sol_restr_all.append(solution)

    hessian_matrix = sm.hessian(func, [x, y], )  # Hessian matrix

    for dot in sol_restr_all:
        hessian_matrix_with_dot = hessian_matrix.subs(dot)
        hessian_matrix_with_dot = np.array(hessian_matrix_with_dot).astype(complex)

        if np.all(np.linalg.eigvals(hessian_matrix_with_dot) > 0):  # матрица положительно определенная, точка минимума
            dot['type'] = 'min'  # добавляем в словарь с соответствующей точкой ее тип
        elif np.all(
                np.linalg.eigvals(hessian_matrix_with_dot) < 0):  # матрица отрицительно определенная, точка максимума
            dot['type'] = 'max'

        else:
            dot['type'] = 'saddle'
        dot['func_value'] = func.subs(dot)

    for dot in sol_restr:
        hessian_matrix_with_dot = hessian_matrix.subs(dot)
        hessian_matrix_with_dot = np.array(hessian_matrix_with_dot).astype(np.float64)

        if np.all(np.linalg.eigvals(hessian_matrix_with_dot) > 0):  # матрица положительно определенная, точка минимума
            dot['type'] = 'min'  # добавляем в словарь с соответствующей точкой ее тип
        elif np.all(
                np.linalg.eigvals(hessian_matrix_with_dot) < 0):  # матрица отрицительно определенная, точка максимума
            dot['type'] = 'max'

        else:
            dot['type'] = 'saddle'
        dot['func_value'] = func.subs(dot)

    output_str = ''
    if sol == []:
        output_str += 'нет точек экстремума'  # !!!
    else:

        for i in range(len(sol_restr_all)):
            output_str += f'({(sol_restr_all[i][x])},{(sol_restr_all[i][y])},' + \
                          f'{(sol_restr_all[i]["func_value"]):}) - {sol_restr_all[i]["type"]} \n'
        sol_restr_all = pd.DataFrame(sol_restr_all)
        sol_restr_all.columns = ['x', 'y', 'type', 'z']
        for i in range(len(sol_restr_all)):
            sol_restr_all.loc[i, ['x', 'y', 'z']] = (sol_restr_all.loc[i, ['x', 'y', 'z']].apply(lambda x: sm.N(x, 4)))

        sol_restr = pd.DataFrame(sol_restr)
        sol_restr.columns = ['x', 'y', 'type', 'z']

    return sol_restr_all, sol_restr
