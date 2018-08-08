from django.urls import path
from .views import CreateView, CreateCartByGetForAnonymous, CreateCartByGetForClient, AllCartsList, AllCartsOfAccount

urlpatterns = [
    path('create/', CreateView.as_view()),
    path('create/anonymous/', CreateCartByGetForAnonymous.as_view()),
    path('create/<int:account_id>/', CreateCartByGetForClient.as_view()),
    path('all/', AllCartsList.as_view()),
    path('all/<int:account_id>/', AllCartsOfAccount.as_view()),
]