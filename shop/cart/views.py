from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .forms import CartForm
from .models import Cart, CartItem
from account.models import Account
#
#
# def create_new_cart_for_account(request):
#     cart = Cart(client=request.user)
#     return cart
#
#
# def check_and_get_account_cartid(request, cartid):
#     cart = get_cart_or_404(cartid)
#     if cart.client == request.user and not cart.is_payed:
#         return cart
#     else:
#         return create_new_cart_for_account(request)
#
#
# def cart_of_account(account):
#     carts = Cart.objects.all().filter(client=account)
#     if len(carts) > 0:
#         for cart in carts:
#             if not cart.is_payed:
#                 return cart
#     return False
#
#
# def get_cartid_of_account(request):
#     cartid = request.session.get('cartid', None)
#     if cartid is not None:
#         cart = check_and_get_account_cartid(request, cartid)
#         return cart
#     else:
#         cart = cart_of_account(request.user)
#         if cart:
#             return cart
#         return create_new_cart_for_account(request)
#
#


def create_new_cart_for_anonymous():
    cart = Cart()
    return cart


def check_and_get_anonymous_cartid(cartid):
    cart = get_cart_or_404(cartid)
    if cart.client is None:
        return cart
    else:
        return create_new_cart_for_anonymous()


def get_cartid_of_anonymous(request):
    cartid = request.session.get('cartid', None)
    if cartid is not None:
        return check_and_get_anonymous_cartid(cartid)

    else:
        return create_new_cart_for_anonymous()


def create_new_cart_for_account(account):
    cart = Cart(client=account)
    return cart


def get_cart_of_account(account):
    carts = Cart.objects.all().filter(client=account)
    if len(carts) > 0:
        for cart in carts:
            if not cart.is_payed:
                return cart
    return create_new_cart_for_account(account)


def get_cartid(request):
    if request.user.is_authenticated:
        cart = get_cart_of_account(request.user)
        return cart
    else:
        cart = get_cartid_of_anonymous(request)
    cart.save()
    request.session['cartid'] = cart.id
    return cart



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


def user_id_is_permitted_to_view(request, account_id):
    if request.user.is_authenticated and (request.user.id == account_id or request.user.is_staff):
        return True
    return False


class AllCartsOfAccountView(TemplateView):

    def get(self, request, account_id, *args, **kwargs):
        if user_id_is_permitted_to_view(request, account_id):
            account = get_account_or_404(account_id)
            carts = Cart.objects.all().filter(client= account)
            return render(request, 'cart/list.html', {'carts': carts})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def cart_belongs_to_user(request, cart):
    cart_account = cart.client
    if cart_account  is not None and request.user.id == cart_account .id:
        return True
    return False


def product_is_already_in_cart(cart, product, count):
    cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_item in cart_items:
        if cart_item.product == product:
            cart_item.count += count
            return cart_item
    return False


def add_product_to_cart(cart, product, count):
    cart_item = product_is_already_in_cart(cart, product, count)
    if not cart_item:
        cart_item = CartItem(cart=cart, product=product, count=count)
    cart_item.save()
    cart.total += count * product.price
    cart.save()


class CartDetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        cart = get_cart_or_404(id)

        cartid_session = request.session.get('cartid', None)
        if cart_belongs_to_user(request, cart) or user_is_staff(request) or cartid_session == id:
            cart_items = CartItem.objects.all().filter(cart__id=id)
            return render(request, 'cart/detail.html', {'cart_items': cart_items, 'cart': cart})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class DeleteCartView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            cart = get_cart_or_404(id)
            cart.delete()
            return HttpResponse('Cart is deleted!') # TODO: REDIRECT USER TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class AddToCartHasCount(TemplateView):

    def get(self, request, id, pid, count, *args, **kwargs):
        from product.views import get_product_or_404
        cart = get_cart_or_404(id)
        product = get_product_or_404(pid)

        cartid_session = request.session.get('cartid', None)
        if cart_belongs_to_user(request, cart) or user_is_staff(request) or cartid_session == id:
            add_product_to_cart(cart, product, count)
            return HttpResponse("product is now added to the cart!")
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class AddToCart(TemplateView):
    def get(self, request, id, pid, *args, **kwargs):
        return HttpResponse("this page does not support get request") #TODO REDIRECT TO ERROR PAGE

    def post(self, request, id, pid, *args, **kwargs):
        from product.views import get_product_or_404
        from product.forms import AddToCartForm
        cart = get_cart_or_404(id)
        product = get_product_or_404(pid)
        cartid_session = request.session.get('cartid', None)

        if cart_belongs_to_user(request, cart) or user_is_staff(request) or cartid_session == id:
            form = AddToCartForm(request.POST)
            if form.is_valid():
                count = form.cleaned_data['count']
                add_product_to_cart(cart, product, count)
                return HttpResponse("product is now added to the cart!") #TODO : REDIRECT TO PRODUCT DETAIL PAGE (OR PERVIUS PAGE)
            return render(request, 'product/detail.html', {'forms': [form], 'submits': ['اضافه به سبذ'],
                                                                                        'methods': ['POST']})
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


from zeep import Client
from django.shortcuts import redirect
MERCHANT = 'e3cdd5aa-9d9b-11e8-922d-000c295eb8fc'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional


class PayView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        cart = get_cart_or_404(id)
        if cart_belongs_to_user(request, cart):
            amount = cart.total
            CallbackURL = 'http://localhost:8000/cart/' + str(id) + '/verify/'  # Important: need to edit for realy server.
            result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
            if result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
            else:
                return HttpResponse('Error code: ' + str(result.Status))
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def substract_cart_items_from_inventory(cart):
    cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_item in cart_items:
        product = cart_item.product
        product.inventory -= cart_item.count
        product.save()


class VerifyView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if request.GET.get('Status') == 'OK':
            cart = get_cart_or_404(id)
            amount = cart.total
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
            if result.Status == 100:
                substract_cart_items_from_inventory(cart)
                cart.is_payed = True
                cart.save()
                return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            elif result.Status == 101:
                return HttpResponse('Transaction submitted : ' + str(result.Status))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed or canceled by user')