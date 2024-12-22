import pandas as pds


def load_data(file_path):
    '''
    Загружает данные в CSV или Excel
    :param file_path: Путь к файлу
    :return: DataFrame
    '''

    if file_path.endswith('.csv'):
        data_ = pds.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data_ = pds.read_excel(file_path)
    else:
        raise ValueError("Неподдерживаемый формат файла. Пожалуйста загрузите CSV или XLSX файл")

    return process_data(data_)


def process_data(data_):
    '''
    Обрабатывает загруженные данные
    :param data_: DataFrame
    :return: обработанный DataFrame
    '''

    data_['value'] = pds.to_numeric(data_['value'], errors='coerce')  # заменяем данные на числа, а ошибки на NaN
    data_['value'] = data_['value'].fillna(0)  # NaN меняем на 0
    return data_