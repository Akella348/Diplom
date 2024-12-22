import matplotlib.pyplot as plt
import pandas as pds

def create_bar_chart(data, x_column, y_column):
    """
    Создает столбчатую диаграмму.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.figure(figsize=(12, 8))

    # Уникальные категории по оси X
    unique_categories = data[x_column].unique()
    num_categories = len(unique_categories)

    # Вычисление ширины столбцов
    bar_width = 1 / num_categories  # Уменьшаем ширину, чтобы столбцы не накладывались

    # Создание смещения для столбцов
    x_positions = []

    for i, category in enumerate(unique_categories):
        category_data = data[data[x_column] == category]
        x_positions.extend(
            [i - (bar_width * (len(category_data) - 1) / 2) + j * bar_width for j in range(len(category_data))])

    # Генерация массива цветов
    color_map = pds.Series(data[y_column]).rank(method='dense').astype(int)
    colors = plt.cm.viridis(color_map / color_map.max())

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
        plt.text(x_positions[i], value + 0.02 * max(data[y_column]), str(value), ha='center', fontsize=6, rotation=60)

    plt.tight_layout()
    plt.show()

def create_line_chart(data, x_column, y_column):
    """
    Создает линейный график.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(data[x_column], data[y_column], marker='o', color='orange')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Line Chart of {y_column} vs {x_column}')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()

def create_histogram(data, column, bins=10):
    """
    Создает гистограмму.

    :param data: DataFrame с данными.
    :param column: Название столбца для построения гистограммы.
    :param bins: Количество корзин для гистограммы.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=bins, color='lightgreen', edgecolor='black')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'Histogram of {column}')
    plt.grid(axis='y', alpha=0.75)
    plt.tight_layout()
    plt.show()
