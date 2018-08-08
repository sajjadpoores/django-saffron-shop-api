from django.urls import path
from .views import CreateView, AllCartsListView, AllCartsOfAccountView, EditCartView, AddToCart, DeleteFromCart

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('<int:id>/edit/', EditCartView.as_view()),
    path('all/', AllCartsListView.as_view()),
    path('all/<int:account_id>/', AllCartsOfAccountView.as_view()),

    path('<int:id>/add/<int:pid>/<int:count>/', AddToCart.as_view()),
    path('<int:id>/delete/<int:pid>/', DeleteFromCart.as_view()),
]