from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QComboBox, QLabel
from source.data_processing import load_data  # импортируем загрузчик данных
import source.visualizations as viz  # импортируем создание графиков
import pandas as pds


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization App")  # название приложения
        self.setGeometry(100, 100, 400, 400)  # размеры главного окна

        layout = QVBoxLayout()  # вертикальная компоновка элементов
        # Кнопка для загрузки данных
        self.load_button = QPushButton("Load Data")  # создаем кнопку
        self.load_button.clicked.connect(self.data_loader)  # связываем нажатие кнопки с загрузкой данных
        layout.addWidget(self.load_button)  # добавляем кнопку в главное окно

        # Метка и выпадающий список для выбора фильтра
        self.unit_label = QLabel("Select Unit Type:")
        layout.addWidget(self.unit_label)
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["DOLLARS(millions)", "COUNT"])
        layout.addWidget(self.unit_combo)

        # Выпадающий список для выбора библиотеки визуализации
        self.library_label = QLabel("Select Visualization Library:")
        layout.addWidget(self.library_label)
        self.library_combo = QComboBox()
        self.library_combo.addItems(["matplotlib", "seaborn", "numpy"])
        layout.addWidget(self.library_combo)

        # Выпадающий список для выбора типа графика
        self.plot_type_label = QLabel("Select Plot Type:")
        layout.addWidget(self.plot_type_label)

        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Bar Chart", "Line Chart"])
        layout.addWidget(self.plot_type_combo)

        # Кнопка для вывода графика
        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)  # связываем кнопку с методом plot_data
        layout.addWidget(self.plot_button)

        container = QWidget()  # создание контейнера для компоновщика
        container.setLayout(layout)  # применение вертикальной компоновки к контейнеру
        self.setCentralWidget(container)  # назначение контейнера центральным

    def data_loader(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data File", "",
                                                   'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_name:
            self.data = load_data(file_name)  # Загружаем данные и сохраняем в атрибуте класса
            print("Data loaded successfully.")  # Сообщение об успешной загрузке данных

    def plot_data(self):
        if self.data.empty:
            print("Сначала загрузите данные.")  # Проверка на наличие загруженных данных
            return

        # Получаем выбранный тип единицы
        selected_unit = self.unit_combo.currentText()
        filtered_data = self.data[self.data['unit'] == selected_unit]  # Фильтруем данные

        if filtered_data.empty:
            print("Нет данных для выбранного типа единицы.")  # Сообщение, если данные отсутствуют
            return

        # Получаем выбранную библиотеку и тип графика
        selected_library = self.library_combo.currentText()
        selected_plot_type = self.plot_type_combo.currentText()

        # Вызов функции для построения графика в зависимости от выбранной библиотеки и типа графика
        if selected_library == "matplotlib":
            if selected_plot_type == "Bar Chart":
                viz.create_bar_chart(filtered_data, x_column='rme_size_grp', y_column='value')
            elif selected_plot_type == "Line Chart":
                viz.create_line_chart(filtered_data, x_column='rme_size_grp', y_column='value')
        # elif selected_library == "seaborn":
        #     if selected_plot_type == "Bar Chart":
        #         viz.create_seaborn_bar_chart(filtered_data, x_column='rme_size_grp', y_column='value')
        #     elif selected_plot_type == "Line Chart":
        #         viz.create_seaborn_line_chart(filtered_data, x_column='rme_size_grp', y_column='value')
        # elif selected_library == "plotly":
        #     if selected_plot_type == "Bar Chart":
        #         viz.create_plotly_bar_chart(filtered_data, x_column='rme_size_grp', y_column='value')
        #     elif selected_plot_type == "Line Chart":
        #         viz.create_plotly_line_chart(filtered_data, x_column='rme_size_grp', y_column='value')
