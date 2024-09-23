from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path('searchDataset/', views.searchDatasets, name='searchDataset'),
]
