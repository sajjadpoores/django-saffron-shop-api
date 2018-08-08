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


def get_cart_or_404(id):
    cart = get_object_or_404(Cart, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return cart


class CreateCartByGetForAnonymousView(TemplateView):
    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            cart = Cart()
            cart.save()
            return HttpResponse('Cart created!')  # TODO: REDIRECT TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class CreateCartByGetForClientView(TemplateView):

    def get(self, request, account_id, *args, **kwargs):
        if user_is_staff(request):
            account = get_account_or_404(account_id)
            cart = Cart(client=account)
            cart.save()
            return HttpResponse('Cart created!')  # TODO: REDIRECT TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class EditCartView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            cart = get_cart_or_404(id)
            form = CartForm(instance=cart)
            return render(request, 'cart/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, id, *args, **kwargs):
        cart = get_cart_or_404(id)
        if user_is_staff(request):
            form = CartForm(request.POST, instance=cart)
            if form.is_valid():
                form.save()
                return HttpResponse('Cart updated!')  # TODO: REDIRECT TO HOMEPAGE
            return render(request, 'cart/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class AllCartsListView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            carts = Cart.objects.all()
            return render(request, 'cart/list.html', {'carts': carts})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def user_is_permitted_to_view(request, account_id):
    if request.user.is_authenticated and (request.user.id == account_id or request.user.is_staff):
        return True
    return False


class AllCartsOfAccountView(TemplateView):
    def get(self, request, account_id, *args, **kwargs):
        if user_is_permitted_to_view(request, account_id):
            account = get_account_or_404(account_id)
            carts = Cart.objects.all().filter(client= account)
            return render(request, 'cart/list.html', {'carts': carts})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE
