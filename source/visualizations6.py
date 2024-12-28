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
    plt.figure(figsize=(12, 8))

    # Уникальные категории по оси X
    unique_categories = data[x_column].unique()
    num_categories = len(unique_categories)

    # Вычисление ширины столбцов
    bar_width = 0.8 / num_categories  # Уменьшаем ширину, чтобы столбцы не накладывались

    # Создание смещения для столбцов
    x_positions = []

    for i, category in enumerate(unique_categories):
        category_data = data[data[x_column] == category]
        x_positions.extend(
            [i - (bar_width * (len(category_data) - 1) / 2) + j * bar_width for j in range(len(category_data))])

    # Генерация массива цветов
    color_map = pds.Series(data[y_column]).rank(method='dense').astype(int)
    colors = plt.cm.winter(color_map / color_map.max())

    # Создание столбчатой диаграммы с различными цветами и заданной шириной столбцов
    plt.bar(x_positions, data[y_column], color=colors, width=bar_width)

    # Настройка меток и заголовка
    plt.xlabel(x_column, fontsize=14, fontweight='bold')
    plt.ylabel(y_column, fontsize=14, fontweight='bold')
    plt.title(f'Bar Chart of {y_column} vs {x_column}', fontsize=18, fontweight='bold')

    # Настройка меток на оси X
    plt.xticks(range(num_categories), unique_categories, rotation=45, fontsize=12)

    # Добавление сетки
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Добавление значений над столбцами для лучшей читаемости
    for i, value in enumerate(data[y_column]):
        plt.text(x_positions[i], value + 0.02 * max(data[y_column]), value, ha='center', fontsize=6, rotation=60)

    plt.tight_layout()
    plt.show()


def create_line_chart(data, x_column, y_column):
    """
    Создает линейный график с помощью Matplotlib.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.figure(figsize=(12, 8))

    unique_categories = data[x_column].unique()
    colors = plt.cm.get_cmap('tab10', len(unique_categories))

    for idx, category in enumerate(unique_categories):
        category_data = data[data[x_column] == category]
        plt.plot(category_data.index, category_data[y_column], marker='o', color=colors(idx), label=category)

    plt.xlabel(x_column, fontsize=14, fontweight='bold')
    plt.ylabel(y_column, fontsize=14, fontweight='bold')
    plt.title(f'Line Chart of {y_column} by {x_column}', fontsize=18, fontweight='bold')

    # Установка меток на оси X только для уникальных категорий
    if len(unique_categories)>1:
        plt.xticks(ticks=range(0, len(data), len(unique_categories)), labels=unique_categories, rotation=45, fontsize=12)
    else:
        plt.xticks(data.index, data[x_column], rotation=45, fontsize=12)
    plt.grid(axis='both', linestyle='--', alpha=0.7)
    plt.legend(title=x_column)
    plt.tight_layout()
    plt.show()


def create_histogram(data, column):
    """
    Создает гистограмму с использованием Matplotlib.

    :param data: DataFrame с данными.
    :param column: Название столбца для построения гистограммы.
    """
    plt.figure(figsize=(12, 8))

    # Разбиваем данные на интервалы и получаем частоты
    counts, bins = pds.cut(data[column], bins=10, retbins=True)
    counts = counts.value_counts().sort_index()

    # Преобразуем интервалы в строки для отображения
    bin_labels = [f'{interval.left:.2f} - {interval.right:.2f}' for interval in counts.index]

    # Генерация массива цветов
    color_map = pds.Series(data[column]).rank(method='dense').astype(int)
    colors = plt.cm.viridis(color_map / color_map.max())

    # Отображение гистограммы
    plt.bar(bin_labels, counts.values, color=colors, edgecolor='black', alpha=0.7)

    # Настройка меток и заголовка
    plt.xlabel(column, fontsize=14, fontweight='bold')
    plt.ylabel('Frequency', fontsize=14, fontweight='bold')
    plt.title(f'Histogram of {column}', fontsize=18, fontweight='bold')

    # Добавление сетки
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Добавление значений над столбцами гистограммы
    for x, count in zip(bin_labels, counts.values):
        plt.text(x, count + 0.02 * max(counts.values), str(count), ha='center', fontsize=10)

    plt.xticks(rotation=45)  # Поворачиваем метки на оси X для лучшей читаемости
    plt.tight_layout()
    plt.show()


def create_contour_plot(data, x_column, y_column, z_column):
    """
    Создает контурный график с использованием Matplotlib и Pandas.

    :param data: Dataframe.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param z_column: Название колонки для оси Z.
    """
    # Извлечение данных из DataFrame по указанным столбцам
    x_data = data[x_column].values
    y_data = data[y_column].values
    z_data = data[z_column].values

    # Проверка на равенство длины массивов
    if len(x_data) != len(y_data) or len(y_data) != len(z_data):
        raise ValueError("Все входные массивы должны иметь одинаковую длину.")

    # Создаем DataFrame из входных данных
    df = pds.DataFrame({'x': x_data, 'y': y_data, 'z': z_data})

    # Создаем сетку для контурного графика
    x_grid = df['x'].unique()
    y_grid = df['y'].unique()

    # Создаем матрицу Z для контурного графика
    z_matrix = pds.DataFrame(index=sorted(y_grid), columns=sorted(x_grid))

    # Заполняем матрицу Z значениями из DataFrame
    for _, row in df.iterrows():
        z_matrix.loc[row['y'], row['x']] = row['z']

    # Заполняем пропуски (NaN) средними значениями соседей
    z_matrix = z_matrix.astype(float).interpolate(method='linear', axis=0).interpolate(method='linear', axis=1)

    # Проверка на наличие NaN в z_matrix перед построением графика
    if z_matrix.isnull().values.any():
        print("Warning: There are NaN values in the z_matrix after interpolation.")

    # Создание контурного графика
    plt.figure(figsize=(10, 6))
    contour = plt.contourf(z_matrix.columns, z_matrix.index, z_matrix.values, levels=15, cmap='viridis')
    plt.colorbar(contour)
    plt.title('Contour Plot')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    plt.show()


def create_seaborn_line_chart(data, x_column, y_column):
    """
    Создает линейный график с использованием Seaborn.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    # Создаем линейный график
    line_chart = sns.lineplot(data=data, x=x_column, y=y_column)

    # Настраиваем заголовок и подписи осей
    line_chart.set_title(f'Line Chart of {y_column} vs {x_column}')
    line_chart.set_xlabel(x_column)
    line_chart.set_ylabel(y_column)

    # Показываем график
    plt.show()


def create_seaborn_bar_chart(data, x_column, y_column,
                             color='blue', alpha=0.8, show_values=True,
                             title=None, xlabel=None, ylabel=None):
    """
    Создает столбчатый график с использованием Seaborn с возможностью настройки.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param color: Цвет столбцов.
    :param alpha: Прозрачность столбцов.
    :param show_values: Показать ли значения над столбцами (True/False).
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    # Создаем столбчатый график
    bar_chart = sns.barplot(data=data, x=x_column, y=y_column, color=color, alpha=alpha)

    # Настраиваем заголовок и подписи осей
    if title:
        bar_chart.set_title(title)
    else:
        bar_chart.set_title(f'Bar Chart of {y_column} vs {x_column}')

    bar_chart.set_xlabel(xlabel if xlabel else x_column)
    bar_chart.set_ylabel(ylabel if ylabel else y_column)

    # Если необходимо, показываем значения над столбцами
    if show_values:
        for p in bar_chart.patches:
            bar_chart.annotate(format(p.get_height(), '.2f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='bottom', fontsize=10)

    # Показываем график
    plt.show()


def create_seaborn_histogram(data, column,
                             bins=10, color='blue', kde=True, alpha=0.6,
                             title=None, xlabel=None, ylabel='Frequency'):
    """
    Создает гистограмму с использованием Seaborn с возможностью настройки.

    :param data: DataFrame с данными.
    :param column: Название колонки для построения гистограммы.
    :param bins: Количество бинов для гистограммы.
    :param color: Цвет гистограммы.
    :param kde: Включить ли кривую плотности (True/False).
    :param alpha: Прозрачность гистограммы.
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    # Создаем гистограмму
    histogram = sns.histplot(data[column], bins=bins, color=color, kde=kde, alpha=alpha)

    # Настраиваем заголовок и подписи осей
    if title:
        histogram.set_title(title)
    else:
        histogram.set_title(f'Histogram of {column}')

    histogram.set_xlabel(xlabel if xlabel else column)
    histogram.set_ylabel(ylabel)

    # Показываем график
    plt.show()


def create_seaborn_contour_plot(data, x_column, y_column, z_column,
                                contour_levels=10, cmap='viridis', point_size=50, alpha=0.7,
                                title=None, xlabel=None, ylabel=None, colorbar_label=None):
    """
    Создает контурный график с использованием Seaborn с возможностью настройки.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param z_column: Название колонки для высоты (значения Z).
    :param contour_levels: Количество уровней контуров.
    :param cmap: Цветовая карта для контуров и точек.
    :param point_size: Размер точек на графике.
    :param alpha: Прозрачность точек.
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    :param colorbar_label: Подпись для цветовой шкалы.
    """
    # Создаем контурный график
    contour_plot = sns.kdeplot(data=data, x=x_column, y=y_column, cmap=cmap, fill=True, levels=contour_levels)

    # Добавляем точки с высотой
    scatter = plt.scatter(data[x_column], data[y_column], c=data[z_column], cmap=cmap, edgecolor='w',
                          s=point_size, alpha=alpha)

    # Настраиваем заголовок и подписи осей
    if title:
        contour_plot.set_title(title)
    else:
        contour_plot.set_title(f'Contour Plot of {y_column} vs {x_column} with height')

    contour_plot.set_xlabel(xlabel if xlabel else x_column)
    contour_plot.set_ylabel(ylabel if ylabel else y_column)

    # Добавляем цветовую шкалу
    if colorbar_label:
        cbar = plt.colorbar(scatter)
        cbar.set_label(colorbar_label)
    else:
        plt.colorbar(scatter, label=z_column)

    # Показываем график
    plt.show()


def create_plotly_line_chart(data, x_column, y_column,
                              color='blue', show_markers=True,
                              title=None, xlabel=None, ylabel=None):
    """
    Создает линейный график с использованием Plotly с возможностью настройки.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param color: Цвет линии.
    :param show_markers: Показать ли маркеры на линии (True/False).
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    fig = px.line(data, x=x_column, y=y_column,
                   line_shape='linear',
                   title=title if title else f'Line Chart of {y_column} vs {x_column}',
                   markers=show_markers)

    fig.update_traces(line=dict(color=color))  # Настройка цвета линии

    fig.update_layout(xaxis_title=xlabel if xlabel else x_column,
                      yaxis_title=ylabel if ylabel else y_column)

    fig.show()


def create_plotly_bar_chart(data, x_column, y_column,
                            show_values=True,
                            title=None, xlabel=None, ylabel=None):
    """
    Создает столбчатый график с использованием Plotly с возможностью настройки.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    :param show_values: Показать ли значения над столбцами (True/False).
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    # Создаем фигуру
    fig = go.Figure()

    # Получаем уникальные категории
    unique_categories = data[x_column].unique()

    # Определяем ширину столбцов
    bar_width = 0.1  # Ширина столбцов
    offset = bar_width * (len(unique_categories) // 2)  # Смещение для центрирования

    # Добавляем столбцы для каждого значения в категории
    for i, category in enumerate(unique_categories):
        filtered_data = data[data[x_column] == category]
        for j, value in enumerate(filtered_data[y_column]):
            # Смещение по оси X для каждого столбца
            x_position = i + j * bar_width
            fig.add_trace(go.Bar(
                x=[x_position],  # Уникальное значение по оси X
                y=[value],  # Значение по оси Y
                name=str(category),  # Название для легенды
                width=bar_width,
            ))

            # Добавляем значение над столбцом
            if show_values:
                fig.add_annotation(x=x_position,
                                   y=value,
                                   text=str(value),
                                   showarrow=False,
                                   font=dict(size=10),
                                   yshift=5)  # Сдвиг по оси Y для размещения над столбцом

    # Настройки графика
    fig.update_layout(title=title if title else f'Bar Chart of {y_column} vs {x_column}',
                      xaxis_title=xlabel if xlabel else x_column,
                      yaxis_title=ylabel if ylabel else y_column,
                      xaxis=dict(tickvals=list(range(len(unique_categories)))),  # Установка меток по оси X
                      xaxis_ticktext=unique_categories,  # Метки для категорий
                      barmode='group',  # Группировка столбцов
                      bargap=0.05)  # Зазор между группами

    fig.show()


def create_plotly_histogram(data, column,
                            bins=10, color='blue', show_kde=True,
                            title=None, xlabel=None, ylabel='Frequency'):
    """
    Создает гистограмму с использованием Plotly с возможностью настройки.

    :param data: DataFrame с данными.
    :param column: Название колонки для построения гистограммы.
    :param bins: Количество бинов для гистограммы.
    :param color: Цвет гистограммы.
    :param show_kde: Включить ли кривую плотности (True/False).
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    fig = px.histogram(data, x=column, nbins=bins,
                       color_discrete_sequence=[color],
                       title=title if title else f'Histogram of {column}')

    if show_kde:
        # Добавляем кривую плотности с помощью Plotly
        fig.add_trace(px.density_contour(data, x=column).data[0])

    fig.update_layout(xaxis_title=xlabel if xlabel else column,
                      yaxis_title=ylabel)

    fig.show()


def create_plotly_contour(data, x_column, y_column, z_column, title='Contour Plot', xlabel='X-axis', ylabel='Y-axis'):
    """
    Создает контурный график с использованием Plotly, фильтруя данные по выбранным столбцам.

    :param data: Полный набор данных (DataFrame).
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    :param z_column: Название столбца для контуров (интенсивности).
    :param title: Заголовок графика.
    :param xlabel: Подпись для оси X.
    :param ylabel: Подпись для оси Y.
    """
    # Фильтрация данных
    x = data[x_column].values
    y = data[y_column].values
    z = data[z_column].values

    # Создание двумерной сетки для интерполяции
    grid_x, grid_y = np.meshgrid(np.linspace(np.min(x), np.max(x), 100),
                                 np.linspace(np.min(y), np.max(y), 100))

    # Интерполяция значений Z
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='linear')

    # Создание контурного графика
    fig = go.Figure(data=
    go.Contour(
        z=grid_z,
        x=np.linspace(np.min(x), np.max(x), 100),
        y=np.linspace(np.min(y), np.max(y), 100),
        colorscale='Viridis',
        colorbar=dict(title='Intensity')
    )
    )

    fig.update_layout(title=title,
                      xaxis_title=xlabel,
                      yaxis_title=ylabel)

    fig.show()

