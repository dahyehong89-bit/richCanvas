from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/delete/<int:pk>/', views.transaction_delete, name='transaction_delete'),
    path('budget/', views.budget_list, name='budget'),
    path('budget/save/', views.budget_save, name='budget_save'),
    path('api/stats/', views.stats_api, name='stats_api'),
]
