from django.urls import path
from .views import CreateView, EditView, ListView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
]