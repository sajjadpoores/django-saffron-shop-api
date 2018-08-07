from django.urls import path
from .views import CreateView, EditView, ListView, DetailView, DeleteView, CategoryCreateView, CategoryEditView, CategoryListView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/delete/', DeleteView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
    path('<int:id>/', DetailView.as_view()),

    path('category/create/', CategoryCreateView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('category/<int:id>/edit/', CategoryEditView.as_view()),
]