from django.urls import path
from . import views
from . import post_view
from .dataset_view import DatasetListAPIView 

urlpatterns = [
    path('protected/', views.my_protected_view, name='my_protected_view'),
    path('post-data/', post_view.handle_post_data, name='handle_post_data'),
    path('api/datasets/', DatasetListAPIView.as_view(), name='dataset_list_api')
]