# activity_logs/urls.py
from django.urls import path
from .views import users_activity_logs

urlpatterns = [
    path('logs/', users_activity_logs, name='users_activity_logs'),
]
