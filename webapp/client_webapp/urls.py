from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.analyze_logs_api, name='analyze_logs'),
    path('containers/', views.get_active_containers, name='get_containers'),
]