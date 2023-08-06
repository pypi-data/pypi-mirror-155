import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def plot(func, interval, df):

    df['size'] = 3
    fig = px.scatter(df, x='point', y='function', size='size',
                     animation_frame='iter',
                     size_max=7,
                     title='График функции')
    x_ax = np.linspace(interval[0], interval[1], 200)
    y_ax = func(x_ax)
    fig.add_trace(go.Scatter(x=x_ax, y=y_ax, name='функция'))

    fig.update_layout(
        xaxis_title='значение х, у.е.',
        yaxis_title='значении f(x) у.е.')
    return fig