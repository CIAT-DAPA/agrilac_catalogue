from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path('searchDataset/', views.searchDatasets, name='searchDataset'),
    path('searchInstitution/', views.searchInstitution, name='searchInstitution'),
    path('search_users/', views.search_users, name='search_users'),
]
