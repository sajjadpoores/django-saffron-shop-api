from django.urls import path
from .views import LoginView, SignupView, LogoutView, EditView, DetailView, ListView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
    path('<int:id>/', DetailView.as_view()),
]