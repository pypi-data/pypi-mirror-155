import pandas as pd


def brent(func, interval, pression=1e-5, max_iter=500,
          flag_results=False, flag_data=False, type_opt='min'):
    """
    Функция поиска экстремума методом Брента.
    :param func: python function
    :param interval: list consisting of float numbers(left and right bounds)
    :param pression: optimization accuracy
    :param max_iter: maximum amount of iterations
    :param flag_results: output of intermediate results
    :param flag_data: recording intermediate results in a dataset
    :param type_opt: ype of extrema: if min:flag_opt=1
                                      if max: flag_opt=-1
    :return: extrema:the point at which the extremum
             df: intermediate results in a dataset
    """
    if type_opt == 'min':
        flag_opt = 1
    else:
        flag_opt = -1

    data = []
    df = pd.DataFrame(columns=['iter', 'point', 'function', 'step_name'])
    step_name = []
    a, b = interval
    gold_const = (3 - 5 ** 0.5) / 2
    remainder = 0.0

    x_largest = x_middle = x_least = a + gold_const * (b - a)
    f_largest = f_middle = f_least = flag_opt * func(x_least)
    if flag_data:
        data = [[0, x_least, func(x_least), '']]
    if flag_results:
        print(f"Номер итерации {0}, точка {x_least}, функция {func(x_least)} .")

    for i in range(1, max_iter + 1):
        middle_point = (a + b) / 2
        tolerance = pression * abs(x_least) + 1e-9

        if abs(x_least - middle_point) > 2 * tolerance - (b - a) / 2:
            p = q = previous_remainder = 0
            if abs(remainder) > tolerance:

                p = ((x_least - x_largest) ** 2 * (f_least - f_middle) -
                     (x_least - x_middle) ** 2 * (f_least - f_largest))

                q = 2 * ((x_least - x_largest) * (f_least - f_middle) -
                         (x_least - x_middle) * (f_least - f_largest))

                if q > 0:
                    p = -p
                else:
                    q = -q

                previous_remainder = remainder
            if abs(p) < 0.5 * abs(q * previous_remainder) and a * q < x_least * q + p < b * q:
                remainder = p / q
                x_new = x_least + remainder
                name_step = 'parabolic'
                step_name.append((name_step))
                if x_new - a < 2 * tolerance or b - x_new < 2 * tolerance:
                    if x_least < middle_point:
                        remainder = tolerance
                    else:
                        remainder = -tolerance

            else:
                name_step = 'golden'
                step_name.append((name_step))
                if x_least < middle_point:
                    remainder = (b - x_least) * gold_const
                else:
                    remainder = (a - x_least) * gold_const
            if abs(remainder) > tolerance:
                x_new = x_least + remainder
            elif remainder > 0:
                x_new = x_least + tolerance
            else:
                x_new = x_least - tolerance

            f_new = flag_opt * func(x_new)


            if f_new <= f_least:
                if x_new < x_least:
                    b = x_least
                else:
                    a = x_least

                x_largest = x_middle
                f_largest = f_middle

                x_middle = x_least
                f_middle = f_least

                x_least = x_new
                f_least = f_new

            else:
                if x_new < x_least:
                    a = x_new
                else:
                    b = x_new

                if f_new <= f_middle:
                    x_largest = x_middle
                    f_largest = f_middle

                    x_middle = x_new
                    f_middle = f_new

                elif f_new <= f_largest:
                    x_largest = x_new
                    f_largest = f_new

        else:
            print('найдено значение с заданной точностью, code 0')
            break
        if flag_data:

            data.append(([i + 1, x_least, func(x_least), step_name[-1]]))
            df = pd.DataFrame(data, columns=['iter', 'point', 'function', 'step_name'])

        if flag_results:
            print(f"Номер итерации {i + 1}, точка {x_least}, функция {func(x_least)}.")

    return x_least, df
