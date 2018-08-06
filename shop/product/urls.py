from django.urls import path
from .views import CreateView, EditView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
]