from django.db import models

class AppCommand(models.Model):
    keyword = models.CharField(max_length=100, verbose_name="Ключове слово")
    app_name = models.CharField(max_length=100, verbose_name="Назва файлу (напр. notepad.exe)")
    path = models.CharField(max_length=500, blank=True, null=True, verbose_name="Шлях (заповниться само)")

    def __str__(self):
        return f"Запуск {self.app_name} за словом '{self.keyword}'"

class VoiceResponse(models.Model):
    keyword = models.CharField(max_length=100, verbose_name="Ключове слово")
    response = models.TextField(verbose_name="Що відповісти")

    def __str__(self):
        return f"Відповідь на '{self.keyword}'"
