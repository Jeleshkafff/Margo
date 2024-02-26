import unittest
from unittest.mock import patch, MagicMock
from Karr import Assistant


class TestAssistant(unittest.TestCase):

    def setUp(self):
        # Создаем экземпляр класса Assistant перед каждым тестом
        self.assistant = Assistant()

    def tearDown(self):
        # Удаляем экземпляр класса Assistant после каждого теста
        self.assistant.root.destroy()

    def test_cleaner(self):
        # Тестирование метода cleaner класса Assistant
        # Проверяем, что метод возвращает правильно очищенный текст
        cleaned_text = self.assistant.cleaner("привет")
        self.assertEqual(cleaned_text, "привет")

    @patch('Karr.datetime.datetime')
    def test_time(self, mock_datetime):
        # Тестирование метода time класса Assistant
        # Проверяем, что метод выводит текущее время в правильном формате
        mock_now = MagicMock()
        mock_now.hour = 12
        mock_now.minute = 0
        mock_datetime.now.return_value = mock_now
        expected_output = "Сейчас 12:0"
        with patch('Karr.Assistant.talk') as mock_talk:
            self.assistant.time()
            mock_talk.assert_called_once_with(expected_output)

    def test_opener(self):
        # Тестирование метода opener класса Assistant
        # Проверяем, что метод открывает правильную ссылку и произносит соответствующее сообщение
        with patch('Karr.webbrowser.open') as mock_webbrowser_open, \
                patch('Karr.Assistant.talk') as mock_talk:
            self.assistant.opener("открой youtube")
            mock_webbrowser_open.assert_called_once_with('https://youtube.com/')
            mock_talk.assert_called_once_with('Открываю youtube')

    def test_hello(self):
        # Тестирование метода hello класса Assistant
        # Проверяем, что метод произносит правильное приветствие
        with patch('Karr.Assistant.talk') as mock_talk:
            self.assistant.hello()
            mock_talk.assert_called_once()

    def test_name(self):
        # Тестирование метода name класса Assistant
        # Проверяем, что метод произносит правильное сообщение о имени
        with patch('Karr.Assistant.talk') as mock_talk:
            self.assistant.name()
            mock_talk.assert_called_once()

if __name__ == '__main__':
    unittest.main()
