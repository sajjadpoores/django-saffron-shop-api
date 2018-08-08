from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import CartForm
from .models import Cart, CartItem
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


def cart_belongs_to_user(request, cart):
    account = cart.client
    if account is not None and request.user.id == account.id:
        return True
    return False


def product_is_already_in_cart(cart, product, count):
    cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_item in cart_items:
        if cart_item.product == product:
            cart_item.count += count
            return cart_item
    return False


class AddToCart(TemplateView):

    def get(self, request, id, pid, count, *args, **kwargs):
        from product.views import get_product_or_404
        cart = get_cart_or_404(id)
        product = get_product_or_404(pid)

        if cart_belongs_to_user(request, cart) or user_is_staff(request): # TODO: OR SESSION[CARTID] OF ANONYUSER == ID
            cart_item = product_is_already_in_cart(cart, product, count)
            if not cart_item:
                cart_item = CartItem(cart=cart, product=product, count=count)
            cart_item.save()
            cart.total += count * product.price
            cart.save()
            return HttpResponse("product is now added to the cart!")
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def get_cart_item_or_404(id):
    cart_item = get_object_or_404(CartItem, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return cart_item


class DeleteFromCart(TemplateView):
    def get(self, request, id, pid, *args, **kwargs):
        cart = get_cart_or_404(id)
        cart_item = list(CartItem.objects.all().filter(cart=id, product__id=pid))

        if len(cart_item):
            cart_item = cart_item[0]
        else:
            return HttpResponse('product is not in cart')  # TODO: REDIRECT TO HOMEPAGE

        if cart_belongs_to_user(request, cart) or user_is_staff(request):  # TODO: OR SESSION[CARTID] OF ANONYUSER == ID
            if cart_item.cart == cart:
                cart.total -= cart_item.count * cart_item.product.price
                cart.save()
                cart_item.delete()
                return HttpResponse('product is now removed from cart!')  # TODO: REDIRECT TO HOMEPAGE
            return HttpResponse('product is not in cart')  # TODO: REDIRECT TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE
