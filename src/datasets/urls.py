from django.urls import path
from . import views

urlpatterns = [
    path('catalogue/', views.catalogue, name='catalogue'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset_detail'),
]
