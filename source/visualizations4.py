import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pds

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


def create_seaborn_bar_chart(data, x_column, y_column):
    """
    Создает столбчатый график с использованием Seaborn.

    :param data: DataFrame с данными.
    :param x_column: Название колонки для оси X.
    :param y_column: Название колонки для оси Y.
    """
    # Создаем столбчатый график
    bar_chart = sns.barplot(data=data, x=x_column, y=y_column)

    # Настраиваем заголовок и подписи осей
    bar_chart.set_title(f'Bar Chart of {y_column} vs {x_column}')
    bar_chart.set_xlabel(x_column)
    bar_chart.set_ylabel(y_column)

    # Показываем график
    plt.show()


def create_seaborn_histogram(data, column):
    """
    Создает гистограмму с использованием Seaborn.

    :param data: DataFrame с данными.
    :param column: Название колонки для построения гистограммы.
    """
    # Создаем гистограмму с кривой плотности
    histogram = sns.histplot(data[column], bins=10, kde=True)

    # Настраиваем заголовок и подписи осей
    histogram.set_title(f'Histogram of {column}')
    histogram.set_xlabel(column)
    histogram.set_ylabel('Frequency')

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
    # Создаем контурный график
    contour_plot = sns.kdeplot(data=data, x=x_column, y=y_column, cmap='viridis', fill=True)

    # Настраиваем заголовок и подписи осей
    contour_plot.set_title(f'Contour Plot of {y_column} vs {x_column}')
    contour_plot.set_xlabel(x_column)
    contour_plot.set_ylabel(y_column)

    # Показываем график
    plt.show()