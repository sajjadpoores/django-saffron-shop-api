from django.urls import path
from .views import CreateView, AllCartsListView, AllCartsOfAccountView, EditCartView, AddToCartHasCount, \
    DeleteFromCart, AddToCart, DeleteCartView, CartDetailView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('<int:id>/', CartDetailView.as_view()),
    path('<int:id>/edit/', EditCartView.as_view()),
    path('<int:id>/delete/', DeleteCartView.as_view()),
    path('all/', AllCartsListView.as_view()),
    path('all/<int:account_id>/', AllCartsOfAccountView.as_view()),

    path('<int:id>/add/<int:pid>/<int:count>/', AddToCartHasCount.as_view()),
    path('<int:id>/add/<int:pid>/', AddToCart.as_view()),
    path('<int:id>/delete/<int:pid>/', DeleteFromCart.as_view()),
]