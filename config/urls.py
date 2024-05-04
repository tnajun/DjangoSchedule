"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib.staticfiles.urls import static
from . import settings
from django.views.generic import RedirectView

urlpatterns = [
    # path('sc/', include('scheduleCalendar.urls')),
    # path('cal/', include('cal.urls')),
    path('admin/', admin.site.urls),
    # path('', include('timeline.urls')),
    # path('contact/', include('contact_form.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    # path('social_app/', include('social_app.urls')),
    # path('accounts/email/', RedirectView.as_view(pattern_name='timeline:index')),
    # path('accounts/inactive/', RedirectView.as_view(pattern_name='timeline:index')),
    # path('accounts/password/change/', RedirectView.as_view(pattern_name='timeline:index')),
    # path('accounts/confirm-email/', RedirectView.as_view(pattern_name='timeline:index')),
    # re_path(r'^accounts/confirm-email/[^/]+/', RedirectView.as_view(pattern_name='timeline:index'), kwargs=None),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    # re_path(r'^accounts/confirm-email/[^/]+/', RedirectView.as_view(pattern_name='timeline:index'), kwargs=None),
    # path('chat/', include('chat.PyChat.urls', namespace='chat')),
    # path('group/', include('group.urls', namespace='group')),
    # path('qa2/', include('QA2.urls', namespace='qa2')),
    # path('user_payment/', include('user_payment.urls')),
    # path('qa/', include('QA.urls', namespace='qa')),
    path('schedule/', include('Schedule.urls')),
    path('', RedirectView.as_view(url='/accounts/home', permanent=False)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('uploads/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]