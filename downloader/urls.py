from django.contrib import admin
from django.urls import path
from .views import index, download_file, bot_visit, mobile_visit, mac_visit

urlpatterns = [
    path('', index),
    path('download/', download_file, name='download'),
    path('bot/', bot_visit, name='bot-visit'),
    path('mobile/', mobile_visit, name='mobile_visit'),
    path('mac/', mac_visit, name='mac_visit'),
    path('admin/', admin.site.urls),
]
