from django.contrib import admin

# Register your models here.
from . models import Relationship
admin.site.register(Relationship)

from .models import CustomUser, AIPrompt
class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('is_therapist', 'is_ai')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AIPrompt)