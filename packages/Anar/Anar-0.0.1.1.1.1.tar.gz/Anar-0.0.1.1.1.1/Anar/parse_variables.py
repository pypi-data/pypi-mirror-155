import sympy as sm
import numpy as np
import re


def parse_variables():
    '''
    Функция возвращает кориеж состоящий из переменных, которые являются sympy symbols
    :return:
    tuple of sympy symbols
    '''
    variables = ''
    flag_vars = False
    while not flag_vars:

        try:
            variables = input('Введите названия переменных, разделенных пробелом: ')
            if '(' in variables or ')' in variables:  # проверка на наличие не предусмотренных символов
                raise Exception
            if ',' in variables:
                variables = sm.parsing.sympy_parser.parse_expr(variables.replace(' ', ''))
                # при наличии ',', приведение к нужному формату убирая пробелы
            else:
                variables = sm.parsing.sympy_parser.parse_expr(variables.replace(' ', ','))
                # приведение к нужному формату
            flag_vars = True

        except Exception:
            print('Ошибка ввода. Введите две переменные через пробел, пример: x y')
    return variables


def parse_function(variables):
    '''
    Запускает парсер функции. Возвращает sympy expression
    :param variables: tuple of sympy symbols
    :return:
    sympy expression
    '''
    function = None
    flag_func = False
    while not flag_func:

        try:
            function = input('Введите функцию: ')
            function = sm.parsing.sympy_parser.parse_expr(function.replace('–', '-'))
            # заменяем минусы
#             check_var = function.free_symbols.difference(variables)
#             # проверяем не содержит ли функция лишние переменные
#             if len(check_var) != 0:
#                 print('Введены лишние переменные')
#                 raise Exception
            flag_func = True
        except Exception:
            print('Ошибка ввода. Введите функцию еще раз: ')
    return function