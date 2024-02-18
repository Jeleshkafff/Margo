import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
import datetime
from random import choice
import webbrowser
import configparser
from queue import Queue

class Assistant:
    def __init__(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('settings.ini')

        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("600x400")
        self.root.configure(bg="#212121")


        self.message_frame = tk.Frame(self.root, bg="#212121")
        self.message_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


        self.text_area = tk.Text(self.message_frame, wrap=tk.WORD, width=60, height=15,
                                 bg="#303030", fg="white", font=("Comfortaa", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.text_area.insert(tk.END, "Здравствуй, меня зовут Марго, я ваш новый голосовой помощник\n", "message")
        self.text_area.insert(tk.END, "К сожалению, сейчас я работаю в тестовом режиме\n", "message")
        self.text_area.insert(tk.END, "Пока что я умею показывать время, открывать нужные вам соц сети, искать ответы в гугл\n", "message")
        self.text_area.insert(tk.END, "Надеюсь я смогу вам помочь 💜\n", "message")
        # Конфигурация тега "message" для установки выравнивания текста
        self.text_area.tag_configure("message", justify="center")

        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            selected_voice = 'VoiceName'
            if selected_voice in voice.name:
                self.engine.setProperty('voice', voice.id)
                break
        self.r = sr.Recognizer()

        self.cmds = {
            ('текущее время', 'сейчас времени', 'который час', "время"): self.time,
            ('привет', 'добрый день', 'здравствуй'): self.hello,
            ('пока', 'прощай'): self.quit,
            ('марго', 'маргошка', 'солнце', 'солнышко', 'моё солнышко', "солнце мое"): self.name,
        }

        self.ndels = ['ладно', 'не могла бы ты', 'пожалуйста', 'сейчас']

        self.commands = [
            'текущее время', 'сейчас времени', "время", 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',
            'привет', 'добрый день', 'здравствуй',
            'пока', 'прощай',
        ]

        self.speech_queue = Queue()

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
        while True:
            text = self.cleaner(self.listen())
            if text != "":
                self.update_chat("Вы: " + text + "\n", sender="user")
                self.update_chat(" " + "\n", sender="user")

            if text.startswith(('открой', 'запусти', 'зайди', 'зайди на', "включи")):
                self.opener(text)

            for tasks, function in self.cmds.items():
                for task in tasks:
                    if fuzz.ratio(task, text) >= 80:
                        function()
                        break

            question_keywords = ['что', 'как', 'почему', 'где', 'когда', 'кто', 'какой', 'какая', 'какие']
            if any(keyword in text for keyword in question_keywords):
                self.talk("Дайте мне немного времени, чтобы найти ответ на ваш вопрос.")
                search_query = text
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
            ('тг', 'телеграм', 'telegram'): 'https://t.me/jeleshkaffff',
            ('музыку','песню','песенку'):choice(['https://www.youtube.com/watch?v=t-Ku3te9lmE&list=PL6c4Rm7WPCMb2jPCUMb3B52UYP59foCyC&index=2&ab_channel=BiaMK', 'https://www.youtube.com/watch?v=L5uV3gmOH9g&ab_channel=BMTHOfficialVEVO', 'https://www.youtube.com/watch?v=jivvlR25Isc&ab_channel=Sen', 'https://www.youtube.com/watch?v=d_HlPboLRL8&ab_channel=iamAURORAVEVO'])
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
            cfr = self.settings['SETTINGS']['fr']
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
        self.root.destroy()

    def hello(self):
        self.talk(choice(['Привет, чем могу помочь?', 'Здраствуйте', 'Приветствую']))

    def name(self):
        self.talk(choice(['Да, я', 'Что?', 'Что хотите?']))

    def talk(self, text):
        self.speech_queue.put(text)

    def speech_synthesis(self):
        while True:
            try:
                text = self.speech_queue.get()
                self.update_chat("Марго: " + text + "\n", sender="bot")
                self.update_chat(" " + "\n", sender="bot")
                self.engine.say(text)
                self.engine.runAndWait()
                self.engine.stop()  # Освободить ресурсы голосового движка
            except Exception as e:
                print("Error in speech synthesis:", e)

    def listen(self):
        with sr.Microphone() as source:
            self.text_area.see(tk.END)
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
            try:
                return self.r.recognize_google(audio, language="ru-RU").lower()
            except Exception as e:
                print(e)
                return ""

    def update_chat(self, message, sender):
        self.text_area.configure(state='normal')  # Enable text entry
        if sender == "user":
            self.text_area.tag_configure("user", justify="right", foreground="white")
            self.text_area.insert(tk.END, message, "user")
        elif sender == "bot":
            self.text_area.tag_configure("bot", justify="left", foreground="#E6BCFF")
            self.text_area.insert(tk.END, message, "bot")
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')  # Disable text entry

    def start(self):
        self.cfile()
        t = Thread(target=self.recognizer)
        t.daemon = True
        t.start()
        t2 = Thread(target=self.speech_synthesis)
        t2.daemon = True
        t2.start()
        self.root.mainloop()

Assistant().start()
