import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt

from Karr import Assistant  # Подключаем ваш класс Assistant из assistant.py

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Голосовой Ассистент")
        self.setGeometry(100, 100, 600, 400)

        self.assistant = Assistant()  # Создаем экземпляр вашего ассистента

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_area = QTextEdit(self)
        self.layout.addWidget(self.text_area)

        self.movie = QMovie("assistant.gif")  # Путь к файлу с гифкой
        self.label_animation = QLabel(self)
        self.label_animation.setMovie(self.movie)
        self.movie.start()

        self.layout.addWidget(self.label_animation)

        self.button_listen = QPushButton("Слушать", self)
        self.layout.addWidget(self.button_listen)
        self.button_listen.clicked.connect(self.listen)

        self.button_stop = QPushButton("Стоп", self)
        self.layout.addWidget(self.button_stop)
        self.button_stop.clicked.connect(self.stop)

        self.dark_theme = QPushButton("Темная тема", self)
        self.layout.addWidget(self.dark_theme)
        self.dark_theme.clicked.connect(self.toggle_dark_theme)

        self.central_widget.setLayout(self.layout)

    def listen(self):
        text = self.assistant.listen()  # Слушаем и возвращаем текст из аудио
        self.text_area.append("Вы: " + text + "\n")
        self.assistant.recognizer(text)  # Передаем текст ассистенту для обработки

    def stop(self):
        self.assistant.engine.stop()  # Останавливаем воспроизведение аудио

    def toggle_dark_theme(self):
        dark_stylesheet = """
            QMainWindow {
                background-color: #333;
                color: #fff;
            }
            QTextEdit {
                background-color: #555;
                color: #fff;
            }
            QPushButton {
                background-color: #666;
                color: #fff;
                border: none;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """
        light_stylesheet = ""
        current_stylesheet = self.styleSheet()
        if current_stylesheet == light_stylesheet or not current_stylesheet:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = AssistantGUI()
    gui.show()
    sys.exit(app.exec_())
