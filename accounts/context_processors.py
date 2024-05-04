
# from .models import Notification
# from django.db.models import Q

# def notifications_count(request):
#     if request.user.is_authenticated:
#         # count = Notification.objects.filter(user=request.user, is_read=False).count()
#         count = Notification.objects.filter(user=request.user, is_read=False).exclude(Q(sender=request.user) | Q(sender=None)).count()
#     else:
#         count = 0

#     return {'notifications_count': count}


# def unread_notifications(request):
#     if request.user.is_authenticated:
#         unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
#     else:
#         unread_notifications = []

#     return {'unread_notifications': unread_notifications}