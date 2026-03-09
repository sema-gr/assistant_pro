import asyncio
import os
import threading
import time
import edge_tts
import pygame

# Ініціалізує модуль mixer у pygame, який відповідає за відтворення звуку
pygame.mixer.init()

# Основна функція, яка генерує голосовий файл з тексту та відтворює його
def speak_task(text):
    # Створює унікальне ім’я файлу, використовуючи поточний час у секундах
    filename = f"voice_{int(time.time())}.mp3"

    # Дозволяє обробляти помилки під час генерації та відтворення голосу, якщо виникне помилка, код переходить у except
    try:
        # Задає голос для синтезу мовлення
        VOICE = "uk-UA-PolinaNeural"

        # Функція асинхронна і її потрібно виконувати через asyncio loop
        async def generate():
            # Створює об’єкт для синтезу мовлення
            communicate = edge_tts.Communicate(text, VOICE)
            # Асинхронно зберігає аудіо у файл filename
            await communicate.save(filename)

        # Створює новий цикл подій для цього потоку
        loop = asyncio.new_event_loop()
        # Встановлює його як поточний
        asyncio.set_event_loop(loop)
        # Запускає асинхронну функцію генерації голосу і чекає на завершення.
        loop.run_until_complete(generate())
        # Закриває цикл подій після завершення роботи, щоб уникнути витоків ресурсів
        loop.close()

        # Перевіряє, чи файл був створений успішно
        if os.path.exists(filename):
            # Завантажує файл у pygame
            pygame.mixer.music.load(filename)
            # Починає відтворення аудіо
            pygame.mixer.music.play()

            # Цикл чекає, поки аудіо відтворюється, щоб програма не завершилась раніше.
            while pygame.mixer.music.get_busy():
                # Пауза, щоб цикл не споживав весь процесор
                time.sleep(0.1)

            # Зупиняє відтворення, якщо воно ще триває
            pygame.mixer.music.stop()
            # Звільняє пам’ять, очищає завантажений файл
            pygame.mixer.music.unload()

            time.sleep(0.2)

            # Видаляє тимчасовий аудіофайл
            os.remove(filename)
            print(f"Файл {filename} видалено")

    # Ловить будь-які помилки під час генерації або відтворення
    except Exception as error:
        print(f"Помилка звуку: {error}")
        # Якщо файл існує, намагається його видалити, щоб не залишати сміття
        if os.path.exists(filename):
            try:
                os.remove(filename)
            # Ігнорує помилки при видаленні файлу
            except:
                pass

# Створює новий потік, щоб виконати speak_task без блокування основного потоку
def speak_async(text):
    threading.Thread(target=speak_task, args=(text,), daemon=True).start()
    # target=… — вказує функцію, яка буде виконана у цьому потоці
    # daemon=True означає, що потік буде автоматично завершений, коли закінчиться основна програма.
    # args=(text,) — передає текст як аргумент функції speak_task


print("Тест speak_task()")
speak_task("Привіт! Це тест синхронного озвучування.")
# Тестування асинхронного виконання
print("Тест speak_async()")
speak_async("Привіт! Це тест асинхронного озвучування.")
# Додаємо невелику паузу, щоб асинхронне озвучування встигло виконатись
time.sleep(5)
print("Тест завершено")