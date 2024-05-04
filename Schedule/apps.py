
# Schedule/apps.py

from django.apps import AppConfig

class ScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Schedule'

    #Googleカレンダーを使う時にこちらを使う。signals.pyにてGoogleカレンダーの情報が取れていた。何らかの理由で使えなくなった。問題点が見つからず
    # def ready(self):
    #     import Schedule.signals
