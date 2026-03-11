import os
import platform
import subprocess
from django.core.management.base import BaseCommand
from core.models import AppCommand, VoiceResponse
from utils.finder import find_app_path
from utils.voice_engine import speak_async
import speech_recognition as sr

class Command(BaseCommand):  # створення Django команди

    def handle(self, *args, **options):  # основний метод, який запускається при виконанні команди
        self.stdout.write(self.style.SUCCESS('Асистент запущений...'))  # повідомлення про запуск
        
        recognizer = sr.Recognizer()  # створення об'єкта розпізнавання мовлення
        mic = sr.Microphone()  # підключення мікрофона
        
        # відкриваємо мікрофон один раз для всього циклу
        with mic as source:  # відкриття потоку мікрофона
            self.stdout.write("Налаштування фонового шуму...")  # повідомлення про налаштування
            recognizer.adjust_for_ambient_noise(source, duration=1)  # адаптація до фонового шуму
            
            self.stdout.write(self.style.SUCCESS("Слухаю..."))  # повідомлення що асистент слухає

            while True:  # нескінченний цикл прослуховування
                try:
                    # запис голосу з мікрофона
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    
                    # розпізнавання мовлення через Google API
                    command_text = recognizer.recognize_google(audio, language='uk-UA').lower()
                    
                    self.stdout.write(f"Ви сказали: {command_text}")  # вивід розпізнаного тексту
                    self.process_command(command_text)  # передача тексту у функцію обробки
                    
                except sr.UnknownValueError:  # якщо мова не розпізнана
                    continue  # перейти до наступної ітерації
                except Exception as e:  # обробка інших помилок
                    self.stdout.write(self.style.WARNING(f"Помилка: {e}"))  # вивід помилки
                    continue  # продовжити роботу

    def process_command(self, text: str):  # функція обробки голосової команди

        text = text.lower().strip()  # переведення тексту у нижній регістр та видалення пробілів

        # якщо команда не містить слово "відкрий"
        if "відкрий" not in text:
            for resp in VoiceResponse.objects.all():  # перебір усіх голосових відповідей
                if resp.keyword and resp.keyword.lower() in text:  # перевірка ключового слова
                    speak_async(resp.response)  # відтворення відповіді голосом
                    return  # завершення функції
            return  # якщо відповідь не знайдена

        found_app = None  # змінна для знайденої програми

        for app in AppCommand.objects.all():  # перебір програм з бази даних
            if app.keyword and app.keyword.lower() in text:  # перевірка ключового слова
                found_app = app  # збереження знайденої програми
                break  # вихід з циклу

        if not found_app:  # якщо програма не знайдена
            speak_async("Я не знайшла такої програми.")  # голосове повідомлення
            return  # завершення функції

        # якщо шлях до програми вже є і файл існує
        if found_app.path and os.path.exists(found_app.path):
            speak_async(f"Відкриваю {found_app.app_name}...")  # повідомлення про запуск
            self.launch_app(found_app.path)  # запуск програми
            return  # завершення функції

        speak_async(f"Шукаю {found_app.app_name}...")  # повідомлення про пошук програми
        print(found_app.app_name)  # вивід назви програми у консоль
        
        found_path = find_app_path(found_app.app_name)  # пошук шляху до програми

        if found_path:  # якщо шлях знайдено
            found_app.path = found_path  # збереження шляху у моделі
            found_app.save()  # збереження у базі даних

            self.launch_app(found_path)  # запуск програми
        else:
            speak_async("Я не змогла знайти програму на цьому комп'ютері.")  # повідомлення про помилку

    def launch_app(self, path):  # функція запуску програми
        try:
            if platform.system() == "Windows":  # перевірка чи система Windows
                os.startfile(path)  # запуск файлу у Windows
            else:
                subprocess.Popen(['open', path])  # запуск у macOS / Linux
        except Exception as e:  # обробка помилок запуску
            self.stdout.write(self.style.ERROR(f"Помилка запуску: {e}"))  # вивід помилки