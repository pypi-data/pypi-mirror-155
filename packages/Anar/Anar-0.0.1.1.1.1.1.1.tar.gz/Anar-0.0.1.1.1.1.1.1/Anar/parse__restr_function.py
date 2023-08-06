import sympy as sm
import numpy as np
import re

def parse__restr_function(variables):
    '''
    Функция возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :param variables:
    :return: dict: key=variables, value=list
    '''
    restr_function = None
    flag_func = False
    while not flag_func:

        try:
            restr_function = input('Введите  огранеичивающую функцию: ')
            restr_function = sm.parsing.sympy_parser.parse_expr(restr_function.replace('–', '-'))
#             check_var = restr_function.free_symbols.difference(variables)
#             if len(check_var) != 0:
#                 print('Введены лишние переменные')
#                 raise Exception
            flag_func = True
        except Exception:
            print('Ошибка ввода. Введите функцию еще раз: ')
    return restr_function