import sympy as sm
import numpy as np
import re

def parse_restriction(variables):
    '''
    Функция возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :param variables:
    :return: dict: key=variables, value=list
    '''
    restr_val = None
    flag_restriction = False
    while not flag_restriction:
        try:
            restrictions = input('Есть ли ограничения ? 1-да/ 0 – нет : ')
            if len(restrictions.strip()) == 1:
                restrictions = int(restrictions)
            else:
                raise Exception

            restr_val = {}
            if restrictions == 1:
                for var in variables:
                    restr_values = input(f'Введите ограничения по {str(var)}, если нет ограничений-введите 0:  -1 1 ')
                    restr_values = restr_values.strip()  # убираем пробелы в конце и начале
                    if restr_values == '0':
                        restr_val[var] = [-np.inf, np.inf]  # при отстутствии ограничений

                    else:
                        restr_values = restr_values.replace(',', ' ')  # проверка вводов
                        restr_values = re.sub(" +", " ", restr_values)  # убираем лишние пробелы

                        restr_val[var] = list(map(int, restr_values.split(' ')))
                        if len(restr_val[var]) != 2:
                            raise Exception
            elif restrictions == 0:
                for var in variables:
                    restr_val[var] = [-np.inf, np.inf]

            else:
                raise Exception

            flag_restriction = True
        except Exception:
            print('Ошибка ввода: ')
    return restr_val
