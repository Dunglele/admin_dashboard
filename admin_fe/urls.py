from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls), # Đổi path để tránh trùng
    path('', include('dashboard.urls')),
]
