# access_requests/urls.py
from django.urls import path
from .views import request_access, review_requests, user_access_requests, process_request, delete_request

urlpatterns = [
    path('request-access/<int:dataset_id>/', request_access, name='request_access'),
    path('review-requests/', review_requests, name='review_requests'),
    path('my-requests/', user_access_requests, name='user_access_requests'),
    path('process-request/<int:request_id>/<str:action>/', process_request, name='process_request'),
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),
]
