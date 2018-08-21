from django.utils import timezone
from django.test import TestCase
from .forms import CartForm
from .models import Cart, CartItem
from account.models import State, City, Account
from product.models import Product, Category
from account.forms import SignupForm
from django.contrib.messages import get_messages
from random import randint


class FormTest(TestCase):
    def test_create_cart(self):
        data = {'create_time': timezone.now(), 'is_payed': False, 'total': 0}
        form = CartForm(data= data)
        self.assertTrue(form.is_valid())

        data = {}
        form = CartForm(data=data)
        self.assertTrue(form.is_valid())
        cart = form.save()

        state = State.objects.create(name='s1')
        city = City.objects.create(name='c1', state=state)

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertTrue(form.is_valid())
        form.save()

        data = {'client': 1}
        form = CartForm(data= data)
        form.is_valid()
        form.save()

        self.assertEqual(Cart.objects.get(pk=2).client.first_name, 'first name')


class ViewTest(TestCase):
    def setUp(self):
        state = State.objects.create(name='خراسان رضوی')
        city = City.objects.create(name='مشهد', state=state)

    def login(self, login_data={'username': 'username', 'password': 'password@123'}):
        response = self.client.get('/account/logout/')

        response = self.client.post('/account/login/', login_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue('عزیز، خوش آمدید' in str(messages[len(messages) - 1]))

    def create_user_and_login(self, username='username'):
        response = self.client.get('/account/logout/')

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500' +
                                                                                            str(randint(100, 999)),
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': username,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        login_data = {'username': username, 'password': 'password@123'}
        account_count = Account.objects.count()
        response = self.client.post('/account/signup/', signup_data)
        self.assertTrue(account_count + 1, Account.objects.count())
        self.login(login_data)

        return login_data

    def test_create_view(self):
        response = self.client.get('/cart/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/cart/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/create/')
        self.assertTemplateUsed(response, 'cart/create.html')

        response = self.client.post('/cart/create/', {'client': 1})
        self.assertEqual(Cart.objects.get(pk=3).client.first_name, 'first name')

    def test_all_carts(self):
        response = self.client.get('/cart/all/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/cart/all/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/cart/all/')
        self.assertTemplateUsed(response, 'cart/list.html')

    def test_all_carts_of_account(self):
        response = self.client.get('/cart/all/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/cart/all/1/')
        self.assertTemplateUsed(response, 'cart/list.html')

        self.create_user_and_login('username2')
        response = self.client.get('/cart/all/2/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/all/3/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/1/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/4/')
        self.assertTemplateNotUsed(response, 'cart/list.html')

    def test_edit_cart(self):
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        cart = Cart.objects.create()
        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/1/edit/')
        self.assertTemplateUsed(response, 'cart/edit.html')

        response = self.client.post('/cart/1/edit/', {'client': 1})

        self.login({'username': 'username', 'password': 'password@123'})
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        response = self.client.post('/cart/1/edit/', {'client': 1})

    def test_add_to_cart_has_count(self):
        response = self.client.get('/cart/1/add/1/2/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'صفحه مورد نظر پیدا نشد.')

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        category = Category.objects.create(name='c1')
        product = Product.objects.create(name='p1', category=category, price=10, description='text')
        cart = Cart.objects.create(client=Account.objects.get(pk=1))

        response = self.client.get('/cart/1/add/1/2/')
        self.assertEqual(CartItem.objects.all().count(), 1)

        self.create_user_and_login()
        response = self.client.get('/cart/1/add/1/2/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        cart = Cart.objects.create(client=Account.objects.get(pk=2))
        response = self.client.get('/cart/2/add/1/2/')
        self.assertEqual(CartItem.objects.all().count(), 2)
        self.assertEqual(Cart.objects.get(pk=2).total, 20)

        cart = Cart.objects.create(client=Account.objects.get(pk=2))
        response = self.client.get('/cart/2/add/1/2/')
        self.assertEqual(CartItem.objects.get(pk=2).count, 4)

        self.login({'username': 'admin', 'password': 'password@123'})
        cart = Cart.objects.create(client=Account.objects.get(pk=2))
        response = self.client.get('/cart/2/add/1/2/')
        self.assertEqual(CartItem.objects.get(pk=2).count, 6)

    def test_delete_from_cart(self):
        response = self.client.get('/cart/1/delete/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'صفحه مورد نظر پیدا نشد.')

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        category = Category.objects.create(name='c1')
        product = Product.objects.create(name='p1', category=category, price=10, description='text')
        cart = Cart.objects.create(client=Account.objects.get(pk=1))
        response = self.client.get('/cart/1/add/1/2/')

        response = self.client.get('/cart/1/delete/1/')
        self.assertEqual(CartItem.objects.all().count(), 0)

        response = self.client.get('/cart/1/add/1/2/')
        self.create_user_and_login()
        response = self.client.get('/cart/1/delete/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        cart = Cart.objects.create(client=Account.objects.get(pk=2))
        response = self.client.get('/cart/2/add/1/2/')
        self.assertEqual(CartItem.objects.all().count(), 2)
        self.assertEqual(Cart.objects.get(pk=1).total, 20)
        response = self.client.get('/cart/2/delete/1/')
        self.assertEqual(CartItem.objects.all().count(), 1)
        self.assertEqual(Cart.objects.get(pk=2).total, 0)

        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/2/add/1/2/')
        response = self.client.get('/cart/2/delete/1/')
        self.assertEqual(Cart.objects.get(pk=2).total, 0)

    def test_add_to_cart(self):
        response = self.client.get('/cart/1/add/1/')
        self.assertEqual(response.status_code, 200)

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        category = Category.objects.create(name='c1')
        product = Product.objects.create(name='p1', category=category, price=10, description='text', photo='1')
        response = self.client.get('/product/1/')
        self.assertEqual(len(response.context['forms']), 1)

        from cart.views import get_cartid
        request = response.wsgi_request
        cartid = get_cartid(request).id
        cart_item = CartItem.objects.create(product=Product.objects.get(pk=1), count=1, cart=Cart.objects.get(pk=cartid))
        cart = Cart.objects.get(pk=1)
        cart.total = 10
        cart.save()

        response = self.client.get('/product/1/')
        self.assertEqual(len(response.context['forms']), 2)

        post_data = {'count': 3}
        response = self.client.post('/cart/1/add/1/', data=post_data)
        self.assertEqual(Cart.objects.get(pk=1).total, 40)

        response = self.client.get('/cart/1/delete/1/')
        self.assertEqual(Cart.objects.get(pk=1).total, 0)

    def test_delete_cart_view(self):
        response = self.client.get('/cart/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/cart/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/cart/1/delete/')

        cart = Cart.objects.create()
        cart.save()

        self.assertEqual(Cart.objects.all().count(), 1)
        response = self.client.get('/cart/' + str(cart.id) + '/delete/')

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'کارت با موفقیت حذف شد.')

    def test_cart_detail_view(self):
        response = self.client.get('/cart/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'صفحه مورد نظر پیدا نشد.')

        from cart.views import get_cartid
        request = response.wsgi_request
        cartid = get_cartid(request).id

        category = Category.objects.create(name='c1')
        product = Product.objects.create(name='p1', category=category, price=10, description='text', photo='1')

        response = self.client.get('/product/1/')
        request = response.wsgi_request
        cartid = get_cartid(request).id
        post_data = {'count': 3}
        response = self.client.post('/cart/' + str(cartid) + '/add/1/', data=post_data)
        self.assertEqual(Cart.objects.get(pk=cartid).total, 30)

        request = response.wsgi_request
        cartid = get_cartid(request).id

        response = self.client.get('/cart/'+ str(cartid) + '/')
        self.assertEqual(response.context['cart'].total, 30)
        self.assertTemplateUsed(response, 'cart/detail.html')

        cart = Cart.objects.create()
        cart_item = CartItem.objects.create(cart=cart, product=product, count=1)

        response = self.client.get('/cart/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()

        from cart.views import get_cartid
        request = response.wsgi_request
        cartid = get_cartid(request).id

        self.assertEqual(cartid, 4)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        request = response.wsgi_request
        cartid = get_cartid(request).id
        response = self.client.get('/cart/' + str(cartid) + '/')
        self.assertEqual(response.context['cart'].total, 0)
        self.assertTemplateUsed(response, 'cart/detail.html')

        self.login()
        request = response.wsgi_request
        cartid = get_cartid(request).id
