from django.urls import path
from . import views
from .views import incoming_data_view

urlpatterns = [
    path('accounts/', views.account_list, name='account-list'),
    path('accounts/<int:pk>/', views.account_detail, name='account-detail'),
    path('destinations/', views.destination_list, name='destination-list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination-detail'),
    path('server/incoming_data/', incoming_data_view, name='incoming_data'),
]