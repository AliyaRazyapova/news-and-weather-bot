from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.message_history, name='history'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
