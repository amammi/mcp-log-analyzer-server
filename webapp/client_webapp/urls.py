from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.log_analyzer_view, name="index"),
    path('api/analyze/', views.analyze_logs_api, name='analyze_logs'),
    path('api/containers/', views.get_active_containers, name='get_containers'),
]