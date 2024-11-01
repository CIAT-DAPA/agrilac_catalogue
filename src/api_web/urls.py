from django.urls import path
from . import views
from . import post_view
from .dataset_view import DatasetListAPIView, DatasetDetailAPIView, DatasetSearchAPIView, DatasetManageAPIView, DatasetCreateAPIView  # Importa la vista de gestión de datasets
from .institution_view import InstitutionListAPIView

urlpatterns = [
    path('protected/', views.my_protected_view, name='my_protected_view'),
    path('post-data/', post_view.handle_post_data, name='handle_post_data'),
    path('api/datasets/', DatasetListAPIView.as_view(), name='dataset_list_api'),
    path('api/datasets/<int:pk>/', DatasetDetailAPIView.as_view(), name='dataset_detail_api'),  # Ruta para detalle de dataset
    path('api/datasets/search/', DatasetSearchAPIView.as_view(), name='dataset_search'),
    path('api/institutions/', InstitutionListAPIView.as_view(), name='institution_list_api'),
    path('api/datasets/create/', DatasetCreateAPIView.as_view(), name='dataset_create_api'),
    path('api/manage/datasets/', DatasetManageAPIView.as_view(), name='dataset_create_api'),  # Ruta para crear datasets
    path('api/manage/datasets/<int:pk>/', DatasetManageAPIView.as_view(), name='dataset_update_delete_api'),  # Ruta para actualizar y eliminar datasets
]
