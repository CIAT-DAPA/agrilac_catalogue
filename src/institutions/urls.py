# institutions/urls.py
from django.urls import path
from .views import institution_partners, institution_detail, remove_partner, institution_list

urlpatterns = [
    path('institution/partners/', institution_partners, name='partners'),
    path('institution/<int:pk>/', institution_detail, name='institution_detail'),
    path('institution/<int:institution_id>/remove-partner/<int:partner_id>/', remove_partner, name='remove_partner'),
    path('institution/add-partner/', institution_partners, name='add_partner'),
    path('institution_list/', institution_list, name='institution_list'),
]