import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from Karr import Assistant  # Подключаем  класс Assistant из assistant.py

class ListenThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant

    def run(self):
        text = self.assistant.listen()  # Слушаем и возвращаем текст из аудио
        self.message_received.emit(text)

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Голосовой Ассистент")
        self.setGeometry(100, 100, 1000, 300)


        self.assistant = Assistant()  # Создаем экземпляр  ассистента

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.message_list = QListWidget(self)
        self.layout.addWidget(self.message_list)

        self.movie = QMovie("sticker.gif")  # Путь к файлу с гифкой
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

    # def start_listening(self):
    #     self.listen_thread = ListenThread(self.assistant)
    #     self.listen_thread.message_received.connect(self.handle_message)
    #     self.listen_thread.start()

    def listen(self):
        text = self.assistant.listen()  # Слушаем и возвращаем текст из аудио
        print(text)
        user_message_item = QListWidgetItem("Вы: " + text + "\n")
        self.message_list.addItem(user_message_item)

        bot_response = self.assistant.recognizer(text)  # Передаем текст ассистенту для обработки
        print(bot_response)
        bot_message_item = QListWidgetItem("Бот: " + bot_response)
        self.message_list.addItem(bot_message_item)
    # def handle_message(self, message):
    #     user_message_item = QListWidgetItem("Вы: " + message)
    #     self.message_list.addItem(user_message_item)
    #     bot_response = self.assistant.recognizer(message)  # Передаем текст ассистенту для обработки
    #     bot_message_item = QListWidgetItem("Бот: " + bot_response)
    #     self.message_list.addItem(bot_message_item)

    def stop(self):
        self.assistant.engine.stop()  # Останавливаем воспроизведение аудио

    def toggle_dark_theme(self):
        dark_stylesheet = """
            QMainWindow {
                background-color: #333;
                color: #fff;
            }
            QListWidget {
                background-color: #555;
                color: #fff;
                border: none;
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