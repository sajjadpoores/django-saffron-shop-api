from django.urls import path
from .views import LoginView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
]