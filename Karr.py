import pyttsx3
import speech_recognition as sr
import colorama
from fuzzywuzzy import fuzz
import datetime
from os import system
import sys
from random import choice
from pyowm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
import configparser
import pyaudio

class Assistant:
    settings = configparser.ConfigParser()
    settings.read('settings.ini')

    config_dict = get_default_config()  # Инициализация get_default_config()
    config_dict['language'] = 'ru'  # Установка языка

    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.text = ''

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час', "время"): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'прощай'): self.quite,
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

        self.num_task = 0
        self.j = 0
        self.ans = ''

    def cleaner(self, text):
        self.text = text

        for i in self.ndels:
            self.text = self.text.replace(i, '').strip()
            self.text = self.text.replace('  ', ' ').strip()

        self.ans = self.text

        for i in range(len(self.commands)):
            k = fuzz.ratio(text, self.commands[i])
            if (k > 70) & (k > self.j):
                self.ans = self.commands[i]
                self.j = k

        return str(self.ans)

    def recognizer(self,text):
        self.text = self.cleaner(self.listen())
        print(self.text)

        if self.text.startswith(('открой', 'запусти', 'зайди', 'зайди на', "включи")):
            self.opener(self.text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task, self.text) >= 80:
                    self.cmds[tasks]()

        self.engine.runAndWait()
        self.engine.stop()
        return ("AbobA")

    def time(self):
        now = datetime.datetime.now()
        self.talk("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def opener(self, task):
        links = {
            ('youtube', 'ютуб', 'ютюб'): 'https://youtube.com/',
            ('вк', 'вконтакте', 'контакт', 'vk'): 'https://vk.com/feed',
            ('браузер', 'интернет', 'browser'): 'https://google.com/',
            ('тг', 'телеграм', 'telegram'): 'https://t.me/jeleshkaffff',
        }
        j = 0
        if 'и' in task:
            task = task.replace('и', '').replace('  ', ' ')
        double_task = task.split()
        if j != len(double_task):
            for i in range(len(double_task)):
                for vals in links:
                    for word in vals:
                        if fuzz.ratio(word, double_task[i]) > 75:
                            webbrowser.open(links[vals])
                            self.talk('Открываю ' + double_task[i])
                            j += 1
                            break

    def cfile(self):
        try:
            cfr = Assistant.settings['SETTINGS']['fr']

        except Exception as e:
            print('Перезапустите Ассистента!', e)


    def quite(self):
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
                self.text = self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
            return self.text


Assistant().cfile()

# while True:
#     Assistant().recognizer()