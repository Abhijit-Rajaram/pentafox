from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('user/', views.user_creation),
    path('delete_user/', views.delete_user),
    path('toggle_status/', views.toggle_status),
    path('role/', views.role),
    
]