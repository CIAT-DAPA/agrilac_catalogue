from django.urls import path
from . import views
from . import post_view
from .dataset_view import DatasetListAPIView, DatasetDetailAPIView,DatasetSearchAPIView  # Importa la vista de detalle
from .institution_view import InstitutionListAPIView

urlpatterns = [
    path('protected/', views.my_protected_view, name='my_protected_view'),
    path('post-data/', post_view.handle_post_data, name='handle_post_data'),
    path('api/datasets/', DatasetListAPIView.as_view(), name='dataset_list_api'),
    path('api/datasets/<int:pk>/', DatasetDetailAPIView.as_view(), name='dataset_detail_api'),  # Nueva ruta
    path('api/datasets/search/', DatasetSearchAPIView.as_view(), name='dataset_search'),
    path('api/institutions/', InstitutionListAPIView.as_view(), name='institution_list_api'),
]
