import numpy as np
import sympy as sm
import pandas as pd

def lagrange(variab, func, restr, restr_func):
    '''
    Поиск локальных экстремумов функции двух переменных с ограничениями (метод Лагранжа);
    :param variab: кортеж состоящий из переменных, которые являются sympy symbols
    :param func: sympy expression
    :param restr: возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :param restr_func: sympy expression
    :return: Список координат и значение функции в точке, для всех точек локальных экстремумов,
     с указанием типа экстремума (минимум, максимум, седловая точка)
    '''
    x, y, lam = sm.symbols('x, y lambda')

    func = func.subs({variab[0]: x, variab[1]: y})  # заменяем переменные во избежание комплексных ответов
    restr_func = restr_func.subs({variab[0]: x, variab[1]: y})
    lagr_func = func + restr_func * lam
    lagr_func

    func = func.subs({variab[0]: x, variab[1]: y})  # заменяем переменные во избежание комплексных ответов
    lagr_func = func + restr_func * lam  # составляем функцию лагранжа
    restr_func = restr_func.subs({variab[0]: x, variab[1]: y})
    variab1_d = sm.diff(lagr_func, x)  # дифференцируем по каждой из переменных
    variab2_d = sm.diff(lagr_func, y)

    sol = sm.solve([variab1_d,
                    variab2_d,
                    restr_func],
                   [x, y, lam], dict=True)  # приравниваем частные производные и ограничивающую функцию к нулю и
    # решаем систему
    for solution in sol:
        if len(solution) < 3:
            sol.remove(solution)
    if sol == []:
        sol_restr_all = 'бесконечное количество решений'
        sol_restr = ''
    else:
        sol_restr = []
        sol_restr_all = []
        for solution in sol:
            if solution[x].is_real and solution[y].is_real:

                if restr[variab[0]][0] <= solution[x] <= restr[variab[0]][1] and \
                        restr[variab[1]][0] <= solution[y] <= restr[variab[1]][1]:
                    sol_restr.append(solution)
                    sol_restr_all.append(solution)
            else:

                sol_restr_all.append(solution)

        hessian_matrix = sm.hessian(lagr_func, [lam, x, y])  # Hessian matrix

        for dot in sol_restr_all:
            if hessian_matrix.subs(dot).det() > 0:  # смотрим знак определителя матрицы
                dot['type'] = 'max'  # добавляем в словарь с соответствующей точкой ее тип
            elif hessian_matrix.subs(dot).det() < 0:  # смотрим знак определителя матрицы
                dot['type'] = 'min'  # добавляем в словарь с соответствующей точкой ее тип
            else:
                dot['type'] = 'saddle'  # добавляем в словарь с соответствующей точкой ее тип
            dot['func_value'] = func.subs(dot)

        for dot in sol_restr:
            hessian_matrix_with_dot = hessian_matrix.subs(dot)
            hessian_matrix_with_dot = np.array(hessian_matrix_with_dot).astype(np.float64)

            if np.all(np.linalg.eigvals(
                    hessian_matrix_with_dot) > 0):  # матрица положительно определенная, точка минимума
                dot['type'] = 'min'  # добавляем в словарь с соответствующей точкой ее тип
            elif np.all(
                    np.linalg.eigvals(
                        hessian_matrix_with_dot) < 0):  # матрица отрицительно определенная, точка максимума
                dot['type'] = 'max'

            else:
                dot['type'] = 'saddle'
            dot['func_value'] = func.subs(dot)
        output_str = ''
        #     for i in range(len(sol_restr)):
        #         output_str += f'({float(sol_restr[i][x]):.3}, {float(sol_restr[i][y]):.3}, ' +\
        #                     f'{float(sol_restr[i]["func_value"]):.3}) - {sol_restr[i]["type"]} \n'

        sol_restr_all = pd.DataFrame(sol_restr_all)

        sol_restr_all.columns = ['x', 'y', 'lam', 'type', 'z']
        sol_restr_all = sol_restr_all.drop(['lam'], axis=1)
        for i in range(len(sol_restr_all)):
            sol_restr_all.loc[i, ['x', 'y', 'z']] = (sol_restr_all.loc[i, ['x', 'y', 'z']].apply(lambda x: sm.N(x, 4)))
        sol_restr = pd.DataFrame(sol_restr)
        sol_restr.columns = ['x', 'y', 'lam', 'type', 'z']
    return sol_restr_all, sol_restr