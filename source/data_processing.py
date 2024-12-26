import pandas as pds


def load_data(file_path):
    """
    Загружает данные в CSV или Excel
    :param file_path: Путь к файлу
    :return: DataFrame
    """

    if file_path.endswith('.csv'):
        data = pds.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pds.read_excel(file_path)
    else:
        raise ValueError("Неподдерживаемый формат файла. Пожалуйста загрузите CSV или XLSX файл")

    return data


def process_data(data, column):
    """
    Обрабатывает загруженные данные
    :param data: DataFrame
    :return: обработанный DataFrame
    """

    # преобразование в числа, ошибки - в NaN и заменяем на 0.
    try:
        data.loc[:, column] = pds.to_numeric(data[column], errors='coerce').fillna(0).astype(int)
        # data.loc[:, column] = data[column].fillna(0).astype(int)
    except Exception as e:
        print(f"Ошибка при обработке столбца {column}: {e}")
    return data


def process_all_data(data):
    """
    Обрабатывает загруженные данные
    :param data: DataFrame
    :return: обработанный DataFrame
    """

    # преобразование в числа, ошибки - в NaN и заменяем на 0.
    try:
        data.loc = pds.to_numeric(data, errors='coerce').fillna(0)
        # data.loc[:, column] = data[column].fillna(0).astype(int)
    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
    return data