from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import CartForm
from .models import Cart
from account.models import Account


def user_is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    return False


class CreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CartForm()
            return render(request, 'cart/create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CartForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Cart created!')  # TODO: REDIRECT TO HOMEPAGE
            return render(request, 'cart/create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def get_account_or_404(id):
    account = get_object_or_404(Account, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return account


class CreateCartByGetForAnonymous(TemplateView):
    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            cart = Cart()
            cart.save()
            return HttpResponse('Cart created!')  # TODO: REDIRECT TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class CreateCartByGetForClient(TemplateView):

    def get(self, request, account_id, *args, **kwargs):
        if user_is_staff(request):
            account = get_account_or_404(account_id)
            cart = Cart(client= account)
            cart.save()
            print(cart.client.first_name)
            return HttpResponse('Cart created!')  # TODO: REDIRECT TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE