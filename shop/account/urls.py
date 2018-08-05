from django.urls import path
from .views import LoginView, SignupView, LogoutView, EditView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<int:id>/edit/', EditView.as_view()),
]