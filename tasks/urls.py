from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_edit'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),
    path('complete/<int:pk>/', views.task_complete, name='task_complete'),
    path('register/', views.register, name='register'),
]