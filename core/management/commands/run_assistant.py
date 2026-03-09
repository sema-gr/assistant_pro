import os
import platform
import subprocess
from django.core.management.base import BaseCommand
from core.models import AppCommand, VoiceResponse
from utils.finder import find_app_path
from utils.voice_engine import speak_async
import speech_recognition as sr

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Асистент запущений...'))
        
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        
        # Відкриваємо мікрофон один раз для всього циклу
        with mic as source:
            self.stdout.write("Налаштування фонового шуму...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.stdout.write(self.style.SUCCESS("Слухаю..."))

            while True:
                try:
                    # Тепер mic знаходиться всередині блоку with, тому помилки не буде
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                    command_text = recognizer.recognize_google(audio, language='uk-UA').lower()
                    
                    self.stdout.write(f"Ви сказали: {command_text}")
                    self.process_command(command_text)
                    
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Помилка: {e}"))
                    continue

    def process_command(self, text: str):

        text = text.lower().strip()

        if "відкрий" not in text:
            for resp in VoiceResponse.objects.all():
                if resp.keyword and resp.keyword.lower() in text:
                    speak_async(resp.response)
                    return
            return

        found_app = None

        for app in AppCommand.objects.all():
            if app.keyword and app.keyword.lower() in text:
                found_app = app
                break

        if not found_app:
            speak_async("Я не знайшла такої програми.")
            return

        if found_app.path and os.path.exists(found_app.path):
            speak_async(f"Відкриваю {found_app.app_name}...")
            self.launch_app(found_app.path)
            return

        speak_async(f"Шукаю {found_app.app_name}...")
        print(found_app.app_name)
        found_path = find_app_path(found_app.app_name)

        if found_path:
            found_app.path = found_path
            found_app.save()

            self.launch_app(found_path)
        else:
            speak_async("Я не змогла знайти програму на цьому комп'ютері.")

    def launch_app(self, path):
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            else:
                subprocess.Popen(['open', path])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка запуску: {e}"))
