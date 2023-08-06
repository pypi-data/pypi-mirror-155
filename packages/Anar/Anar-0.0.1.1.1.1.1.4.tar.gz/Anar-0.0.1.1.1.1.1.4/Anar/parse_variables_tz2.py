import sympy as sm
import re


def parse_variables_tz2():
    '''
    Функция возвращает кориеж состоящий из переменной, которая является sympy symbol
    :return:
    tuple of sympy symbol
    '''

    variables = input('Введите названия переменной ')

    return variables


def parse_function_tz2(variables):
    '''
    Запускает парсер функции. Возвращает sympy expression
    :param variables: tuple of sympy symbols
    :return:
    sympy expression
    '''

    function = input('Введите функцию: ')
    function = sm.parsing.sympy_parser.parse_expr(function.replace('–', '-'))
    function = sm.lambdify(variables, function)

    return function


def parse_restriction_tz2(variables):
    '''
    Функция возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :param variables:
    :return: dict: key=variables, value=list
    '''

    restr_values = input(f'Введите ограничения  ')
    restr_values = restr_values.strip()  # убираем пробелы в конце и начале

    restr_values = restr_values.replace(',', ' ')  # проверка вводов
    restr_values = re.sub(" +", " ", restr_values)  # убираем лишние пробелы
    restr_val = restr_values
    restr = restr_val.split()
    interval = [float(restr[0]), float(restr[1])]
    return interval


def parser_task_gr():
    '''
    Функция почередно проверяющая все входные данные
    :return: tuple containing of: tuple, sympy expression, dict
    '''
    variables = parse_variables_tz2()
    func = parse_function_tz2(variables)
    interval = parse_restriction_tz2(variables)
    return variables, func, interval