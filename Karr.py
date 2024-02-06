import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
import webbrowser
import configparser

class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = {'language': 'ru'}  # Simplified language configuration

    def __init__(self):
        # Initialize pyttsx3 engine with desired voice
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')  # Get list of available voices
        # Print available voices for reference
        for voice in voices:
            selected_voice = 'VoiceName'
            if selected_voice in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        self.r = sr.Recognizer()
        # Rest of the __init__ method remains unchanged

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час', "время"): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'прощай'): self.quit,
            ('марго', 'маргошка', 'солнце', 'солнышко', 'моё солнышко', "солнце мое"): self.name,
        }

        self.ndels = ['ладно', 'не могла бы ты', 'пожалуйста',
                      'текущее', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', "время", 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'прощай',
        ]

    def cleaner(self, text):
        for i in self.ndels:
            text = text.replace(i, '').strip()
            text = text.replace('  ', ' ').strip()

        ans = text

        for command in self.commands:
            similarity_ratio = fuzz.ratio(text, command)
            if similarity_ratio > 70 and similarity_ratio > getattr(self, 'j', 0):
                ans = command
                self.j = similarity_ratio

        return ans

    def recognizer(self):
        text = self.cleaner(self.listen())
        print(text)

        if text.startswith(('открой', 'запусти', 'зайди', 'зайди на', "включи")):
            self.opener(text)

        for tasks, function in self.cmds.items():
            for task in tasks:
                if fuzz.ratio(task, text) >= 80:
                    function()
                    break

        self.engine.runAndWait()

        # Now let's handle answering questions using Google
        question_keywords = ['что', 'как', 'почему', 'где', 'когда', 'кто', 'какой', 'какая', 'какие']
        if any(keyword in text for keyword in question_keywords):
            # Speak out the question to let the user know the assistant is processing it
            self.talk("Дайте мне немного времени, чтобы найти ответ на ваш вопрос.")
            # Use Google to search for an answer to the question
            search_query = text  # You can refine the query if needed
            search_url = "https://www.google.com/search?q=" + search_query
            webbrowser.open(search_url)

    def time(self):
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https://vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
        }

        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()

        for i in range(len(double_task)):
            for vals, link in links.items():
                if any(fuzz.ratio(word, double_task[i]) > 75 for word in vals):
                    webbrowser.open(link)
                    self.talk('Открываю ' + double_task[i])
                    return

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']
            if cfr != 1:
                with open('settings.ini', 'w', encoding='UTF-8') as file:
                    file.write('[SETTINGS]\ncountry = RU\nplace = Moskov\nfr = 1')
        except Exception as e:
            print('Перезапустите Ассистента!', e)
            with open('settings.ini', 'w', encoding='UTF-8') as file:
                file.write('[SETTINGS]\ncountry = RU\nplace = Moskov\nfr = 1')

    def quit(self):
        self.talk(choice(['Надеюсь мы скоро увидимся', 'Рада была помочь', 'Пока пока', 'Я отключаюсь']))
        self.engine.stop()
        system('cls')
        sys.exit(0)

    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))

    def name(self):
        self.talk(choice(['Да, я', 'Что?', 'Хи-хи, что хотите?', "м? котя"]))

    def talk(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print(colorama.Fore.LIGHTGREEN_EX + "Я вас слушаю...")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                return self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
                return ""


Assistant().cfile()

while True:
    Assistant().recognizer()