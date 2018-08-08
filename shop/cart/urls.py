from django.urls import path
from .views import CreateView, CreateCartByGetForAnonymousView, CreateCartByGetForClientView, AllCartsListView,\
    AllCartsOfAccountView, EditCartView

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('create/anonymous/', CreateCartByGetForAnonymousView.as_view()),
    path('create/<int:account_id>/', CreateCartByGetForClientView.as_view()),
    path('<int:id>/edit/', EditCartView.as_view()),
    path('all/', AllCartsListView.as_view()),
    path('all/<int:account_id>/', AllCartsOfAccountView.as_view()),
]