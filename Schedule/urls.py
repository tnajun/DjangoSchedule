# Schedule/urls.py

from django.urls import path
from .views import  schedule_meeting_in_django, create_event_in_django, edit_schedule, delete_schedule

app_name = 'schedule'

urlpatterns = [
    path('view_schedule_django/create_event_django/', create_event_in_django, name='create_event_django'),
    path('view_schedule_django/<slug:slug>/', schedule_meeting_in_django, name='view_schedule_django'),
    path('edit_schedule/', edit_schedule, name='edit_schedule'),
    path('delete-schedule/<int:schedule_id>/', delete_schedule, name='delete_schedule')
]


    # path('therapist_calendar/<int:therapist_id>/', views.therapist_calendar_view, name='therapist_calendar'),
    # path('view_schedule/<slug:slug>/', schedule_meeting, name='view_schedule'),
    # path('schedule_meeting/<int:therapist_id>/', ScheduleMeetingView.as_view(), name='schedule_meeting'),
    # path('create_event/', CreateEventFunc, name='create_event'),
    # path('test_schedule_meeting/test_create_event/', test_create_event, name='test_create_event'),
    # path('test_schedule_meeting/', test_schedule_meeting_view, name='test_schedule_meeting'),