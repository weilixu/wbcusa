from django.conf.urls import include, url
from .views import DashboardView
from django.urls import path

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]
