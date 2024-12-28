import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pds
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata

graphics_list = ["Bar Chart", "Line Chart", "Histogram", "Contour"]

def create_bar_chart(data, x_column, y_column):
    """
    Создает столбчатую диаграмму функциями из Matplotlib.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.bar(data[x_column], data[y_column])
    plt.show()

def create_line_chart(data, x_column, y_column):
    """
    Создает линейный график.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.plot(data[x_column], data[y_column])
    plt.show()

def create_histogram(data, column, bins=10):
    """
    Создает гистограмму.

    :param data: DataFrame с данными.
    :param column: Название столбца для построения гистограммы.
    :param bins: Количество корзин для гистограммы.
    """
    plt.hist(data[column], bins=bins)
    plt.show()


def create_contour_plot(data, x_column, y_column, z_column):
    """
    Создает контурный график.

    :param data: DataFrame.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param z_column: Название колонки для оси Z.
    """
    plt.tricontourf(data[x_column], data[y_column], data[z_column], levels=15, cmap='viridis')
    plt.colorbar()
    plt.show()


def create_seaborn_bar_chart(data, x_column, y_column):
    """
    Создает столбчатый график с использованием Seaborn.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    # Создаем столбчатый график
    sns.barplot(data=data, x=x_column, y=y_column)

    # # Настраиваем заголовок и подписи осей
    # bar_chart.set_title(f'Bar Chart of {y_column} vs {x_column}')
    # bar_chart.set_xlabel(x_column)
    # bar_chart.set_ylabel(y_column)

    # Показываем график
    plt.show()


def create_seaborn_line_chart(data, x_column, y_column):
    """
    Создает линейный график с использованием Seaborn.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    # Создаем линейный график
    sns.lineplot(data=data, x=x_column, y=y_column)

    # # Настраиваем заголовок и подписи осей
    # line_chart.set_title(f'Line Chart of {y_column} vs {x_column}')
    # line_chart.set_xlabel(x_column)
    # line_chart.set_ylabel(y_column)

    # Показываем график
    plt.show()


def create_seaborn_histogram(data, column):
    """
    Создает гистограмму с использованием Seaborn.

    :param data: DataFrame с данными.
    :param column: Название колонки для построения гистограммы.
    """
    # Создаем гистограмму с кривой плотности
    sns.histplot(data[column], bins=10, kde=True)

    # # Настраиваем заголовок и подписи осей
    # histogram.set_title(f'Histogram of {column}')
    # histogram.set_xlabel(column)
    # histogram.set_ylabel('Frequency')

    # Показываем график
    plt.show()


def create_seaborn_contour_plot(data, x_column, y_column, z_column):
    """
    Создает контурный график с использованием Seaborn.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param z_column: Название колонки для оси Y.
    """
    sns.kdeplot(data=data, x=x_column, y=y_column, cmap='viridis', fill=True)
    plt.scatter(data[x_column], data[y_column], c=data[z_column], cmap='viridis', edgecolor='w', s=50)
    plt.colorbar(label=z_column)
    plt.show()


def create_plotly_bar_chart(data, x_column, y_column):
    """
    Создает столбчатый график с использованием Plotly.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    fig = px.bar(data, x=x_column, y=y_column)
    fig.show()


def create_plotly_line_chart(data, x_column, y_column):
    """
    Создает линейный график с использованием Plotly.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    fig = px.line(data, x=x_column, y=y_column)
    fig.show()


def create_plotly_histogram(data, column):
    """
    Создает гистограмму с использованием Plotly.

    :param data: DataFrame с данными.
    :param column: Название колонки для построения гистограммы.
    """
    fig = px.histogram(data, x=column)
    fig.show()


def create_plotly_contour(data, x_column, y_column, z_column):
    """
    Создает контурный график с использованием Plotly.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    :param z_column: Название столбца для контуров (интенсивности).
    """
    x = data[x_column].values
    y = data[y_column].values
    z = data[z_column].values

    grid_x, grid_y = np.meshgrid(np.linspace(np.min(x), np.max(x), 100),
                                   np.linspace(np.min(y), np.max(y), 100))
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

    fig = go.Figure(data=go.Contour(z=grid_z, x=grid_x[0], y=grid_y[:, 0], colorscale='Viridis'))
    fig.show()


