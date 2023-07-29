from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.message_history, name='history'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('response/', views.bot_response_list, name='response_list'),
    path('response/<int:template_id>/edit/', views.bot_response_edit, name='response_edit'),
]
