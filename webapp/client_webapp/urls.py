from django.urls import path
from . import views

urlpatterns = [
    path("", views.log_analyzer_view, name="index"),
    path('api/analyze/', views.analyze_logs_api, name='analyze_logs'),
    path('api/containers/', views.get_active_containers, name='get_containers'),
]