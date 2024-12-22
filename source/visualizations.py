import matplotlib.pyplot as plt

def create_bar_chart(data, x_column, y_column):
    """
    Создает столбчатую диаграмму.

    :param data: DataFrame с данными.
    :param x_column: Название столбца для оси X.
    :param y_column: Название столбца для оси Y.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_column], data[y_column], color='skyblue')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Bar Chart of {y_column} vs {x_column}')
    plt.xticks(rotation=45)
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
