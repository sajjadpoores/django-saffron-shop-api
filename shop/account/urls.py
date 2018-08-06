from django.urls import path
from .views import LoginView, SignupView, LogoutView, EditView, DetailView, ListView, DeactivateView, ActivateView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('all/', ListView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
    path('<int:id>/deactivate/', DeactivateView.as_view()),
    path('<int:id>/activate/', ActivateView.as_view()),
    path('<int:id>/', DetailView.as_view()),
]