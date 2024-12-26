import sys
from PyQt5.QtWidgets import QApplication  # pyqt5 аналог tkinter, но посовременнее и удобнее. создадим диалоговое окно
from source.gui3 import MainWindow # gui импортируем из написанного файла

if __name__ == "__main__":
    app = QApplication(sys.argv)  # создаем объект для управления приложением,
                                  # sys.argv передает аргументы командной строки
    window = MainWindow()  # главное окно приложения
    window.show()  # отображение главного окна
    sys.exit(app.exec_())  # запуск цикла обработки событий(нажатие кнопок и т.п.) и завершение приложения
