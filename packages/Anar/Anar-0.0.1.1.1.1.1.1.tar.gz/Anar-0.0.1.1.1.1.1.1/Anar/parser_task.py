def parser_task1():
    '''
    Функция почередно проверяющая все входные данные
    :return: tuple containing of: tuple, sympy expression, dict
    '''
    variables = parse_variables()
    func = parse_function(variables)
    restr = parse_restriction(variables)
    return variables, func, restr