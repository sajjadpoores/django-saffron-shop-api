from django.urls import path
from .views import HomeView, AdminView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', AdminView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]