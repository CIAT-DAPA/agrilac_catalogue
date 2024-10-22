from django.urls import path
from . import views
from . import post_view

urlpatterns = [
    path('protected/', views.my_protected_view, name='my_protected_view'),
    path('post-data/', post_view.handle_post_data, name='handle_post_data'),
]