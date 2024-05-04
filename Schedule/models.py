
# Schedule/models.py

from django.db import models
from django.conf import settings  # Import to use custom user model



class ScheduleAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, '月曜日'),
        (1, '火曜日'),
        (2, '水曜日'),
        (3, '木曜日'),
        (4, '金曜日'),
        (5, '土曜日'),
        (6, '日曜日'),
    )

    therapist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_therapist': True})
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('therapist', 'day_of_week', 'start_time', 'end_time')




class Schedule(models.Model):
    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_therapist': True},
        verbose_name='Therapist'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()




class TherapistGoogleCalendar(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    google_calendar_id = models.CharField(max_length=255, blank=True, null=True)
    google_access_token = models.CharField(max_length=255, blank=True, null=True)
    google_refresh_token = models.CharField(max_length=255, blank=True, null=True)
    google_token_expiry = models.DateTimeField(blank=True, null=True)
    google_credentials = models.TextField(blank=True, null=True)  # For storing the full credentials JSON

    class Meta:
        permissions = [
            ('is_therapist', 'Can access therapist features'),
        ]


# from django.utils import timezone
# import pytz
# import datetime

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_created')
    therapist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events_scheduled', limit_choices_to={'is_therapist': True}, verbose_name='Therapist')
    summary = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = 'Events'

    @classmethod
    def create_event_in_django(cls, user, therapist, summary, start_time, end_time):
        event = cls(user=user, therapist=therapist, summary=summary, start_time=start_time, end_time=end_time)
        event.save()
        return event

    @classmethod
    def get_events_in_django(cls, therapist, time_min, time_max):
        events = cls.objects.filter(therapist=therapist, start_time__gte=time_min, end_time__lte=time_max)
        return events
