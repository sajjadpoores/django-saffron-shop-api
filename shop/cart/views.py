from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import CartForm
from .models import Cart, CartItem
from account.models import Account


def get_redirect_path(request):
    if request.POST.get('path'):
        return request.POST.get('path')
    elif request.GET.get('path'):
        return request.GET.get('path')
    else:
        return '/home'


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

            cart = get_cartid(request)

            return render(request, 'cart/create.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CartForm(request.POST)
            if form.is_valid():
                form.save()

                messages.success(request, 'کارت با موفقیت ایجاد شد.')
                return redirect('/cart/all/')

            cart = get_cartid(request)

            return render(request, 'cart/create.html', {'form': form, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def get_account_or_404(id):
    account = get_object_or_404(Account, pk=id)
    return account


def get_cart_or_404(id):
    cart = get_object_or_404(Cart, pk=id)
    return cart


class EditCartView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            cart = get_cart_or_404(id)
            form = CartForm(instance=cart)

            account_cart = get_cartid(request)

            return render(request, 'cart/edit.html', {'form': form, 'cartid': account_cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, id, *args, **kwargs):
        cart = get_cart_or_404(id)
        if user_is_staff(request):
            form = CartForm(request.POST, instance=cart)
            if form.is_valid():
                form.save()

                messages.success(request, 'کارت با موفقیت ویرایش شد.')
                return redirect('/cart/all/')

            account_cart = get_cartid(request)

            return render(request, 'cart/edit.html', {'form': form, 'cartid': account_cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class AllCartsListView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            carts = Cart.objects.all()

            cart = get_cartid(request)

            return render(request, 'cart/list.html', {'carts': carts, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def user_id_is_permitted_to_view(request, account_id):
    if request.user.is_authenticated and (request.user.id == account_id or request.user.is_staff):
        return True
    return False


class AllCartsOfAccountView(TemplateView):

    def get(self, request, account_id, *args, **kwargs):
        if user_id_is_permitted_to_view(request, account_id):
            account = get_account_or_404(account_id)
            carts = Cart.objects.all().filter(client= account)

            cart = get_cartid(request)
            return render(request, 'cart/list.html', {'carts': carts, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def cart_belongs_to_user(request, cart):
    cart_account = cart.client
    if cart_account is not None and request.user.id == cart_account.id:
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

            account_cart = get_cartid(request)

            return render(request, 'cart/detail.html', {'cart_items': cart_items, 'cart': cart,
                                                        'cartid': account_cart .id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class DeleteCartView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            cart = get_cart_or_404(id)
            cart.delete()

            messages.success(request, 'کارت با موفقیت حذف شد.')
            redirect_path = get_redirect_path(request)
            return redirect(redirect_path)

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class AddToCartHasCount(TemplateView):

    def get(self, request, id, pid, count, *args, **kwargs):
        from product.views import get_product_or_404
        cart = get_cart_or_404(id)
        product = get_product_or_404(pid)

        cartid_session = request.session.get('cartid', None)
        if cart_belongs_to_user(request, cart) or user_is_staff(request) or cartid_session == id:
            add_product_to_cart(cart, product, count)
            return HttpResponse("product is now added to the cart!")
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class AddToCart(TemplateView):
    def get(self, request, id, pid, *args, **kwargs):
        return HttpResponse("this page does not support get request")

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

                if count < 1:
                    messages.error(request, 'تعداد باید یک یا بیشتر از یک باشد.')
                    return redirect('/product/' + str(pid) + '/')

                add_product_to_cart(cart, product, count)
                messages.success(request, 'محصول به سبد اضافه شد.')

                redirect_path = get_redirect_path(request)
                return redirect(redirect_path)

            account_cart = get_cartid(request)

            return render(request, 'product/detail.html', {'forms': [form], 'submits': ['اضافه به سبذ'],
                                                           'methods': ['POST'], 'cartid': account_cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def get_cart_item_or_404(id):
    cart_item = get_object_or_404(CartItem, pk=id)
    return cart_item


class DeleteFromCart(TemplateView):
    def get(self, request, id, pid, *args, **kwargs):
        cart = get_cart_or_404(id)
        cart_item = list(CartItem.objects.all().filter(cart=id, product__id=pid))

        if len(cart_item):
            cart_item = cart_item[0]
        else:
            messages.error(request, 'محصول در سبد نیست.')
            redirect_path = get_redirect_path(request)
            return redirect(redirect_path)

        if cart_belongs_to_user(request, cart) or user_is_staff(request) or cart.client == None:
            if cart_item.cart == cart:
                cart.total -= cart_item.count * cart_item.product.price
                cart.save()
                cart_item.delete()

                messages.success(request, 'محصول از سبد حذف شد.')
                redirect_path = get_redirect_path(request)
                return redirect(redirect_path)

            messages.error(request, 'محصول در سبد نیست.')
            redirect_path = get_redirect_path(request)
            return redirect(redirect_path)

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


from zeep import Client
from django.shortcuts import redirect
MERCHANT = 'YOUR MERCHANT'
# amount = 1000  # Toman / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید."  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional


class PayView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        cart = get_cart_or_404(id)
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        if cart_belongs_to_user(request, cart):
            amount = cart.total
            CallbackURL = 'http://localhost:8000/cart/' + str(id) + '/verify/'  # edit for realy server.
            result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
            if result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
            else:
                messages.error(request, 'خطا در اتصال به صفحه پرداخت.')
                return redirect('/home/')
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def substract_cart_items_from_inventory(cart):
    cart_items = CartItem.objects.all().filter(cart=cart)
    for cart_item in cart_items:
        product = cart_item.product
        product.inventory -= cart_item.count
        product.save()


class VerifyView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')

        if request.GET.get('Status') == 'OK':
            cart = get_cart_or_404(id)
            amount = cart.total
            result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
            if result.Status == 100:

                substract_cart_items_from_inventory(cart)
                cart.is_payed = True
                cart.save()

                messages.success(request, 'پرداخت با موفقیت انجام شد.')
                return  redirect('/cart/' + str(id) + '/')
            elif result.Status == 101:

                messages.success(request, 'پرداخت شما ثبت شد.')
                return redirect('/cart/' + str(id) + '/')
            else:
                messages.error(request, 'پرداخت صورت نگرفت.')
                return redirect('/cart/' + str(id) + '/')
        else:

            messages.error(request, 'پرداخت صورت نگرفت.')
            return redirect('/cart/' + str(id) + '/')
