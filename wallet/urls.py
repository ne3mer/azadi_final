from django.urls import path

from . import views

urlpatterns = [
    # ... other URL patterns ...
    path('request_withdrawal/', views.request_withdrawal, name='request_withdrawal'),
    path('process_withdrawal_request/<int:request_id>/', views.process_withdrawal_request,
         name='process_withdrawal_request'),

]
