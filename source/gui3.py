from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QComboBox, QLabel, QMessageBox
from source.data_processing import load_data, process_data, process_all_data  # импортируем загрузчик данных
import source.visualizations4 as viz  # импортируем создание графиков
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

        # Метка и выпадающий список для выбора фильтра по оси X
        self.x_label = QLabel("Select X Column:")
        layout.addWidget(self.x_label)
        self.x_combo = QComboBox()
        layout.addWidget(self.x_combo)

        # Выпадающий список для выбора фильтрации по X
        self.x_filter_label = QLabel("Select X Filter Value:")
        layout.addWidget(self.x_filter_label)
        self.x_filter_combo = QComboBox()
        layout.addWidget(self.x_filter_combo)

        # Метка и выпадающий список для выбора фильтра по оси Y
        self.y_label = QLabel("Select Y Column:")
        layout.addWidget(self.y_label)
        self.y_combo = QComboBox()
        layout.addWidget(self.y_combo)

        # Подключаем обработчики событий для обновления фильтров
        self.x_combo.currentIndexChanged.connect(self.update_filters_x)

        # Выпадающий список для выбора библиотеки визуализации
        self.library_label = QLabel("Select Visualization Library:")
        layout.addWidget(self.library_label)
        self.library_combo = QComboBox()
        self.library_combo.addItems(["matplotlib", "seaborn", "plotly"])  # Добавление библиотек
        layout.addWidget(self.library_combo)

        # Выпадающий список для выбора типа графика
        self.plot_type_label = QLabel("Select Plot Type:")
        layout.addWidget(self.plot_type_label)
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(viz.graphics_list)  # Добавление типов графиков
        layout.addWidget(self.plot_type_combo)

        # Метка и выпадающий список для выбора столбца Z
        self.z_label = QLabel("Select Z Column:")  # добавляем метку для Z
        self.z_label.setVisible(False)  # скрываем метку по умолчанию
        layout.addWidget(self.z_label)
        self.z_combo = QComboBox()  # создаем выпадающий список для Z
        self.z_combo.setVisible(False)  # скрываем его по умолчанию
        layout.addWidget(self.z_combo)

        # Подключаем обработчик для изменения видимости Z ComboBox
        self.plot_type_combo.currentIndexChanged.connect(self.update_z_combobox_visibility)

        # Кнопка для вывода графика
        self.plot_button = QPushButton("Plot Data")
        self.plot_button.clicked.connect(self.plot_data)  # связываем кнопку с методом plot_data
        layout.addWidget(self.plot_button)

        container = QWidget()  # создание контейнера для компоновщика
        container.setLayout(layout)  # применение вертикальной компоновки к контейнеру
        self.setCentralWidget(container)  # назначение контейнера центральным


    def data_loader(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Data File", "",
                                                   'Excel Files (*.xlsx);;CSV Files (*.csv)')
        if file_name:
            try:
                self.data = load_data(file_name)  # Загружаем данные и сохраняем в атрибуте класса
                print("Data loaded successfully.")  # Сообщение об успешной загрузке данных
                self.update_comboboxes()  # Обновляем выпадающие списки на основе загруженных данных
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")


    def update_comboboxes(self):
        # Обновление выпадающих списков на основе загруженных данных
        if self.data is not None:
            columns = set(self.data.columns)  # Получаем уникальные названия столбцов
            self.x_combo.clear()  # Очищаем старые элементы
            self.x_combo.addItems(columns)  # Добавляем новые элементы

            self.y_combo.clear()  # Очищаем старые элементы
            self.y_combo.addItems(columns)  # Добавляем новые элементы

            self.z_combo.clear()  # Очищаем старые элементы
            self.z_combo.addItems(columns)  # Добавляем новые элементы

            # Обновляем фильтры после обновления столбцов
            self.update_filters_x()
            self.update_z_combobox_visibility()  # Обновляем видимость Z ComboBox


    def update_z_combobox_visibility(self):
        # Обновление видимости Z ComboBox в зависимости от выбранного типа графика
        selected_plot_type = self.plot_type_combo.currentText()
        if selected_plot_type == "Contour":
            self.z_label.setVisible(True)
            self.z_combo.setVisible(True)
        else:
            self.z_label.setVisible(False)
            self.z_combo.setVisible(False)

    def update_filters_x(self):
        x_column = self.x_combo.currentText()
        print(f"Updating filters for X column: {x_column}")

        if x_column and self.data is not None:
            # Получаем уникальные значения и преобразуем их в строки
            unique_x_values = set(self.data[x_column].dropna())
            print(f"Unique X values: {unique_x_values}")

            # Преобразуем значения в строки
            unique_x_values_str = [str(value) for value in unique_x_values]

            self.x_filter_combo.clear()
            self.x_filter_combo.addItem("Все")
            self.x_filter_combo.addItems(sorted(unique_x_values_str))

    def plot_data(self):
        if self.data is None or self.data.empty:
            print("Сначала загрузите данные.")
            return

        # Получаем выбранные столбцы для осей X и Y
        x_column = self.x_combo.currentText()
        y_column = self.y_combo.currentText()
        z_column = self.z_combo.currentText() if self.z_combo.isVisible() else ""

        # Получаем выбранную библиотеку и тип графика
        selected_library = self.library_combo.currentText()
        selected_plot_type = self.plot_type_combo.currentText()

        # Проверяем, что выбранные столбцы не пустые
        if selected_plot_type == "Contour":
            if x_column == "" or y_column == "" or z_column == "":
                print("Пожалуйста, выберите столбцы для осей X, Y, Z.")
                return
        if x_column == "" or y_column == "":
            print("Пожалуйста, выберите столбцы для осей X и Y.")
            return

        # Получаем выбранные значения для фильтрации
        x_filter_value = self.x_filter_combo.currentText()

        # Фильтруем данные
        all_data = self.data.copy()  # копируем датасет
        if x_filter_value == "Все":
            filtered_data = all_data  # Если выбрано "Все", используем все данные
        else:
            filtered_data = all_data[all_data[x_column] == x_filter_value]

        # Проверяем, есть ли данные после фильтрации
        if filtered_data.empty:
            print("Нет данных для выбранных фильтров.")
            return

        # Обрабатываем данные по выбранному Y
        try:
            # Убедитесь, что вы возвращаете DataFrame, а не Series
            filtered_data = process_data(filtered_data, y_column)  # Обработка выбранного Y
            if self.z_combo.isVisible():
                filtered_all_data = process_all_data(all_data)  # Обработка Z
                # Передаем данные в виде DataFrame

        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")
            return



        # Вызов функции для построения графика в зависимости от выбранной библиотеки и типа графика
        try:
            if selected_library == "matplotlib":
                if selected_plot_type == "Bar Chart":
                    viz.create_bar_chart(filtered_data, x_column=x_column, y_column=y_column)
                elif selected_plot_type == "Line Chart":
                    viz.create_line_chart(filtered_data, x_column=x_column, y_column=y_column)
                elif selected_plot_type == "Histogram":
                    viz.create_histogram(filtered_data, y_column)
                elif selected_plot_type == "Contour":
                    viz.create_contour_plot(filtered_all_data, x_column, y_column, z_column)
            elif selected_library == "seaborn":
                if selected_plot_type == "Bar Chart":
                    viz.create_seaborn_bar_chart(filtered_data, x_column=x_column, y_column=y_column)
                elif selected_plot_type == "Line Chart":
                    viz.create_seaborn_line_chart(filtered_data, x_column=x_column, y_column=y_column)
                elif selected_plot_type == "Histogram":
                    viz.create_seaborn_histogram(filtered_data, y_column)
                elif selected_plot_type == "Contour":
                    viz.create_seaborn_contour_plot(filtered_all_data, x_column, y_column, z_column)
            # elif selected_library == "plotly":
            #     if selected_plot_type == "Bar Chart":
            #         viz.create_plotly_bar_chart(filtered_data, x_column=x_column, y_column=y_column)
            #     elif selected_plot_type == "Line Chart":
            #         viz.create_plotly_line_chart(filtered_data, x_column=x_column, y_column=y_column)
        except Exception as e:
            print(f"Error occurred while plotting: {e}")

