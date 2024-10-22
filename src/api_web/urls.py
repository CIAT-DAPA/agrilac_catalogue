from django.urls import path
from . import views

urlpatterns = [
    path('protected/', views.my_protected_view, name='my_protected_view'),
]