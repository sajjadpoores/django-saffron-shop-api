from django.urls import path
from .views import CreateView, EditView, ListView, DetailView, DeleteView, CategoryCreateView, CategoryEditView, \
    CategoryListView, CategoryDetailView, CategoryDeleteView, CategoryProductsView, SearchView, SearchInCategory

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/delete/', DeleteView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
    path('<int:id>/', DetailView.as_view()),
    path('<str:search_string>/search/', SearchView.as_view()),

    path('<int:id>/<str:search_string>/search/', SearchInCategory.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/all/', CategoryListView.as_view()),
    path('category/<int:id>/delete/', CategoryDeleteView.as_view()),
    path('category/<int:id>/edit/', CategoryEditView.as_view()),
    path('category/<int:id>/', CategoryDetailView.as_view()),
    path('category/<int:id>/products/', CategoryProductsView.as_view()),
]