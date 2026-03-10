import os
import platform 
import subprocess

def find_app_path(app_name: str):  # функція пошуку шляху до програми

    system = platform.system()  # визначає назву поточної ОС

    # перевіряє чи назва закінчується на .exe
    if app_name.lower().endswith(".exe"):
        app_name = app_name[:-4]  # видаляє .exe з назви

    try:  # блок обробки можливих помилок
        # вибір команди пошуку залежно від ОС
        if system == "Windows":
            command = ["where", app_name]  # команда Windows для пошуку програм
        else:
            command = ["which", app_name]  # команда Linux / macOS

        result = subprocess.run(  # запускає системну команду
            command,  # команда для виконання
            capture_output=True,  # зберігає результат виконання
            text=True  # повертає результат у текстовому форматі
        )

        # перевіряє чи команда виконалась успішно і повернула результат
        if result.returncode == 0 and result.stdout.strip():
            path = result.stdout.strip().split("\n")[0].strip()  # бере перший знайдений шлях
            if os.path.exists(path):  # перевіряє чи файл існує
                return path  # повертає знайдений шлях

    except:  # якщо виникла помилка
        pass  # ігнорує її

    # список папок для ручного пошуку
    if system == "Windows":
        search_dirs = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),  # папка Program Files
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),  # папка 32-bit програм
            os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32"),  # системні програми
        ]

        extensions = [".exe"]  # розширення виконуваних файлів у Windows

    else:  # для Linux та macOS
        search_dirs = [
            "/usr/bin",  # стандартна папка програм
            "/usr/local/bin",  # локально встановлені програми
            "/Applications",  # папка програм у macOS
            os.path.expanduser("~/Applications"),  # папка програм користувача
        ]

        extensions = ["", ".app"]  # можливі формати програм

    for root_dir in search_dirs:  # перебирає всі папки пошуку

        if not os.path.exists(root_dir):  # перевіряє чи папка існує
            continue  # якщо ні — переходить до наступної

        for root, dirs, files in os.walk(root_dir):  # проходить по всіх підпапках

            for file in files:  # перебирає всі файли
                for ext in extensions:  # перевіряє можливі розширення
                    if file.lower() == app_name.lower() + ext:  # порівнює назву файлу
                        return os.path.join(root, file)  # повертає повний шлях до файлу

            # обмежує глибину пошуку до 3 рівнів папок
            if root.count(os.sep) - root_dir.count(os.sep) > 3:
                dirs[:] = []  # зупиняє подальший пошук у глибших папках

    return None  # повертає None якщо програму не знайдено