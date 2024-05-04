from django.urls import path
from . import views
# from .views import AIPromptUpdateView

app_name = 'accounts'

urlpatterns = [
    path('home', views.home, name='home'),
    # path('edit-aiprompt/', views.edit_aiprompt, name='edit_aiprompt'),
    # path('edit-aiprompt/', AIPromptUpdateView.as_view(), name='edit_aiprompt')
    path('edit/', views.edit, name='edit'),
    path('userlist/', views.userlistview, name='userlist'),
    path('therapists/', views.therapistlistview, name='therapist-list'),
    path('ais/', views.aiuserlistview, name='ai-user-list'),
    # path('testuserlist/', views.testuserlistview, name='testuserlist'),
    path('mk_relation/<int:pk>/', views.mk_relation, name='mk_relation'), # 追加
    path('rm_relation/<int:pk>/', views.rm_relation, name='rm_relation'), # 追加
    path('follower/', views.follower, name='follower'),
    path('following/', views.following, name='following'),
    # path('mental_check/', views.mental_check, name='mental_check'),
    # path('<slug:slug>/mental/', views.UserEmotionView.as_view(), name='user_emotion'),
    path('<slug:slug>/add_review/', views.add_review, name='add_review'),
    path('<slug:slug>/', views.detail, name='detail'),

    # path('notifications/', views.notifications, name='notifications'),
    # path('notifications/read/<int:notification_id>/', views.read_notification, name='read_notification'),
    # path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
]


