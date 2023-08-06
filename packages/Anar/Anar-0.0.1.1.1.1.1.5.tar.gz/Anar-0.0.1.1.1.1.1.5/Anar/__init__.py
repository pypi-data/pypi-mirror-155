from . import Lagrange

Lagrange.__doc__ = """
Поиск локальных экстремумов функции двух переменных с ограничениями (метод Лагранжа);
:param variab: кортеж состоящий из переменных, которые являются sympy symbols
:param func: sympy expression
:param restr: возвращает словарь, где ключом выступают названия переменных,
значениями являются списки, с ограничивающими интервалами
:param restr_func: sympy expression
:return: Список координат и значение функции в точке, для всех точек локальных экстремумов,
с указанием типа экстремума (минимум, максимум, седловая точка)
    
Anastaisha Kalmykova [https://pypi.org/project/Anar/]
anariem@mail.ru
"""

from .Lagrange import *

# """
# Функция поиска экстремума методом Брента.
# :param func: python function
# :param interval: list consisting of float numbers(left and right bounds)
# :param pression: optimization accuracy
# :param max_iter: maximum amount of iterations
# :param flag_results: output of intermediate results
# :param flag_data: recording intermediate results in a dataset
# :param type_opt: ype of extrema: if min:flag_opt=1
#                                       if max: flag_opt=-1
#     :return: extrema:the point at which the extremum
#              df: intermediate results in a dataset
#
#     Anastaisha Kalmykova [https://pypi.org/project/Anar/]
#     anariem@mail.ru
# """
# __author__ = 'Anastaisha Kalmykova'
# from Anar import brent
#
# """
#     Функция поиска экстремума функции одной переменной методом золотого сечения
#     :param func: python function
#     :param interval: list consisting of float numbers(left and right bounds)
#     :param pression: optimization accuracy
#     :param max_iter: maximum amount of iterations
#     :param flag_results: flag: output of intermediate results
#     :param flag_data: flag: recording intermediate results in a dataset
#     :param type_opt: type of extrema: if min:flag_opt=1
#                                       if max: flag_opt=-1
#     :return: extrema:the point at which the extremum
#              df: intermediate results in a dataset
#     Anastaisha Kalmykova [https://pypi.org/project/Anar/]
#     anariem@mail.ru
# """
# __author__ = 'Anastaisha Kalmykova'
# from Anar import golden_ratio
#
# '''
#     Функция возвращает кориеж состоящий из переменной, которая является sympy symbol
#     :return:
#     tuple of sympy symbol
#     Anastaisha Kalmykova [https://pypi.org/project/Anar/]
#     anariem@mail.ru
# '''
# __author__ = 'Anastaisha Kalmykova'
# from Anar import parse_variables_tz2
#
# """
#     Функция поиска экстремума функции методом парабол
#     :param func: python function
#     :param interval: list consisting of float numbers(left and right bounds)
#     :param pression: optimization accuracy
#     :param max_iter: maximum amount of iterations
#     :param flag_results: output of intermediate results
#     :param flag_data: recording intermediate results in a dataset
#     :param type_opt: type of extrema: if min:flag_opt=1
#                                       if max: flag_opt=-1
#     :return: extrema:the point at which the extremum
#              df: intermediate results in a dataset
#     Anastaisha Kalmykova [https://pypi.org/project/Anar/]
#     anariem@mail.ru
# """
# __author__ = 'Anastaisha Kalmykova'
# from Anar import parabolic_interpolation
#
#      """
#      Функция отрисовки графиков функции двух переменных с отображением точек экстремума
#      :param variab: кортеж состоящий из переменных, которые являются sympy symbols
#      :param func: sympy expression
#      :param restr: возвращает словарь, где ключом выступают названия переменных,
#      значениями являются списки, с ограничивающими интервалами
#      :param dots: pd.Dataframe, состоящий из точек экстремума и их типа. Столбцы: x, y, type, z
#      :return: go.Figure содержаший два графика: поверхность функции и линии уровня
#     Anastaisha Kalmykova [https://pypi.org/project/Anar/]
#     anariem@mail.ru
#     """
# __author__ = 'Anastaisha Kalmykova'
# from Anar import plot
#
#
# from Anar import gradient_descent_fixed
# from Anar import local_extrema
# from Anar import gradient_descent_fixed
# from Anar import parse__restr_function
# from Anar import parse_restriction
# from Anar import parse_variables
# from Anar import parser_task
# from Anar import plot
# from Anar import plot_tz2


