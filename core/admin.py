from django.contrib import admin
from core.models import AppCommand, VoiceResponse

# Register your models here.
admin.site.register(AppCommand)
admin.site.register(VoiceResponse)