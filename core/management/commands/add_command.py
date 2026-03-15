from core.models import AppCommand
from utils.voice_engine import speak_async

def get_voice_input(source, recognizer, timeout=5):
    try:
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=5)
        text = recognizer.recognize_google(audio, language='uk-UA').lower()
        return text
    except Exception:
        return None

def add_new_app_command_voice(source, recognizer):
    # 1. Ключове слово
    speak_async("Щоб додати команду, скажіть ключове слово")
    keyword = get_voice_input(source, recognizer)
    
    if not keyword:
        speak_async("Я не почула слово. Спробуйте ще раз.")
        return

    speak_async(f"Ваше слово {keyword}. Підтвердити?")
    confirm = get_voice_input(source, recognizer)

    if confirm != "так":
        speak_async("Дію скасовано")
        return

    # 2. Назва додатка
    speak_async("Тепер скажіть назву файлу додатка")
    app_name = get_voice_input(source, recognizer)
    
    if not app_name:
        speak_async("Назву не розпізнано.")
        return

    # Очищення назви від пробілів та обробка "крапки"
    app_name = app_name.replace(" крапка ", ".").replace(" ", "")

    speak_async(f"Назва додатка {app_name}. Підтвердити?")
    confirm_app = get_voice_input(source, recognizer)

    if confirm_app != "так":
        speak_async("Додавання скасовано")
        return

    # 3. Збереження в Django
    AppCommand.objects.create(
        keyword=keyword,
        app_name=app_name
    )
    
    speak_async(f"Ваша команда {keyword} додана")
    print(f"Успішно додано в базу: {keyword} -> {app_name}")
