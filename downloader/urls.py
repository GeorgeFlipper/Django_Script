from django.contrib import admin
from django.urls import path, include
from .views import download_file, mobile_visit, mac_visit, home

urlpatterns = [
    path('', home, name='home'),
    path('captcha/', include('captcha.urls')),
    path('download/', download_file, name='download'),
    path('mobile/', mobile_visit, name='mobile_visit'),
    path('mac/', mac_visit, name='mac_visit'),
    path('admin/', admin.site.urls),
]
