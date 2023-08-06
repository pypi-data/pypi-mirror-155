import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import sympy as sm
import pandas as pd

np.seterr(all='ignore')


def plot(variab, func, restr, dots):
    """
    Функция отрисовки графиков функции двух переменных с отображением точек экстремума
    :param variab: кортеж состоящий из переменных, которые являются sympy symbols
    :param func: sympy expression
    :param restr: возвращает словарь, где ключом выступают названия переменных,
    значениями являются списки, с ограничивающими интервалами
    :param dots: pd.Dataframe, состоящий из точек экстремума и их типа. Столбцы: x, y, type, z
    :return: go.Figure содержаший два графика: поверхность функции и линии уровня
    """

    x, y = variab
    if isinstance(dots, pd.DataFrame):
        if restr[x] == [-np.inf, np.inf]:  # определяем ограничения по осям
            x_min = float(dots.x.min())
            x_max = float(dots.x.max())

            x_min = x_min - max((x_max - x_min) * 0.1, 1)  # во избежание отрисовки точек на границах графика
            x_max = x_max + max((x_max - x_min) * 0.1, 1)
        else:
            x_min = restr[x][0]
            x_max = restr[x][1]

        if restr[y] == [-np.inf, np.inf]:
            y_min = float(dots.y.min())
            y_max = float(dots.y.max())
            y_min = y_min - max((y_max - y_min) * 0.1, 1)
            y_max = y_max + max((y_max - y_min) * 0.1, 1)
        else:
            y_min = restr[y][0]
            y_max = restr[y][1]

        cnt_dots = 100
        # возвращаем sympy функцию к python функции,  в которую можно передать х,у позиционно
        func = sm.lambdify([x, y], func)
        # значения для подстановки в функцию
        x, y = np.linspace(x_min, x_max, cnt_dots), np.linspace(y_min, y_max, cnt_dots)

        z = np.zeros((cnt_dots, cnt_dots))
        for i in range(cnt_dots):
            for j in range(cnt_dots):
                z[i, j] = func(x[i], y[j])  # значения функции

        fig = make_subplots(rows=1, cols=2,
                            specs=[[{'is_3d': True}, {'is_3d': False}]],
                            subplot_titles=('Поверхность', 'Линии уровня'))  # создаем фигуру
        fig.add_trace(go.Surface(z=z.T, x=x, y=y, colorscale='pinkyl', opacity=0.7),
                      1, 1)  # добавляем саму поверхность функции
        fig.add_trace(go.Scatter3d(z=dots.z.astype(float), x=dots.x.astype(float),
                                   y=dots.y.astype(float), showlegend=False, mode='markers'), 1, 1)  # точки экстремума
        fig.add_trace(go.Contour(z=z.T, x=x, y=y, showscale=False, colorscale='pinkyl'),
                      1, 2)  # линии уровня
        fig.add_trace(go.Scatter(x=dots.x.astype(float), y=dots.y.astype(float),
                                 showlegend=False, mode='markers'), 1, 2)  # точки экстремума

    else:
        cnt_dots = 101
        # возвращаем sympy функцию к python функции,  в которую можно передать х,у позиционно
        func = sm.lambdify([x, y], func)
        # значения для подстановки в функцию
        x, y = np.linspace(-1, 1, cnt_dots), np.linspace(-1, 1, cnt_dots)  # !!!

        z = np.zeros((cnt_dots, cnt_dots))
        for i in range(cnt_dots):
            for j in range(cnt_dots):
                #                 if y[j]==0:  #!!!
                #                     z[i, j] = np.nan
                #                 else:

                z[i, j] = func(x[i], y[j])  # значения функции
        fig = make_subplots(rows=1, cols=2,
                            specs=[[{'is_3d': True}, {'is_3d': False}]],
                            subplot_titles=('Поверхность', 'Линии уровня'))  # создаем фигуру
        fig.add_trace(go.Surface(z=z.T, x=x, y=y, colorscale='pinkyl', opacity=0.7),
                      1, 1)  # добавляем саму поверхность функции

        fig.add_trace(go.Contour(z=z.T, x=x, y=y, showscale=False, colorscale='pinkyl'),
                      1, 2)  # линии уровня

        fig.update_layout(scene=dict(
            xaxis_title='X у. е.',
            yaxis_title='Y у. е.',
            zaxis_title='Z у. е.')  # подписи осей

        )
        fig.update_xaxes(title_text="X у. е.", row=1, col=2)
        fig.update_yaxes(title_text="Y у. е.", row=1, col=2)

    return fig