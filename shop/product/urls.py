from django.urls import path
from .views import CreateView, EditView, ListView, DetailView, DeleteView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/delete/', DeleteView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
    path('<int:id>/', DetailView.as_view()),
]