
# Schedule/admin.py

from django.contrib import admin
from .models import Schedule, TherapistGoogleCalendar

admin.site.register(Schedule)

@admin.register(TherapistGoogleCalendar)
class TherapistGoogleCalendarAdmin(admin.ModelAdmin):
    list_display = ('user', 'google_calendar_id', 'google_token_expiry')
    search_fields = ('user__username', 'google_calendar_id')
    ordering = ('user',)



from .models import Event  # Event モデルをインポート
class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'therapist', 'summary', 'start_time', 'created_at']  # 表示したいフィールドをリストに指定
# Event モデルを管理者サイトで表示
admin.site.register(Event, EventAdmin)


from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ScheduleAvailability


class ScheduleAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'day_of_week', 'start_time', 'end_time', 'edit_availability')
    list_filter = ('therapist', 'day_of_week')
    search_fields = ('therapist__username', 'day_of_week')

    def edit_availability(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return mark_safe(f'<a href="{url}">Edit</a>')
    edit_availability.short_description = 'Edit Availability'

    def has_change_permission(self, request, obj=None):
        if request.user.is_therapist:  # is_therapist フラグが True の場合のみ許可
            return True
        return False

admin.site.register(ScheduleAvailability, ScheduleAvailabilityAdmin)