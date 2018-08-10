from django.utils import timezone
from django.test import TestCase
from .forms import CartForm
from .models import Cart, CartItem
from account.models import State, City, Account
from product.models import Product, Category
from account.forms import SignupForm


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
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'logged in', response.content)

    def create_user_and_login(self, username='username'):
        response = self.client.get('/account/logout/')

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
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
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/cart/create/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/create/')
        self.assertTemplateUsed(response, 'cart/create.html')

        response = self.client.post('/cart/create/', {})
        self.assertEqual(Cart.objects.get(pk=1).client, None)

        response = self.client.post('/cart/create/', {'client': 1})
        self.assertEqual(Cart.objects.get(pk=2).client.first_name, 'first name')

    def test_all_carts(self):
        response = self.client.get('/cart/all/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/cart/all/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/cart/all/')
        self.assertTemplateUsed(response, 'cart/list.html')

    def test_all_carts_of_account(self):
        response = self.client.get('/cart/all/1/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/cart/all/1/')
        self.assertTemplateUsed(response, 'cart/list.html')

        self.create_user_and_login('username2')
        response = self.client.get('/cart/all/2/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/1/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/all/3/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/1/')
        self.assertTemplateUsed(response, 'cart/list.html')

        response = self.client.get('/cart/all/4/')  # TODO: CHECK REDIRECTION WHEN ERROR PAGE CREATED
        self.assertTemplateNotUsed(response, 'cart/list.html')

    def test_edit_cart(self):
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        cart = Cart.objects.create()
        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/cart/1/edit/')
        self.assertTemplateUsed(response, 'cart/edit.html')

        response = self.client.post('/cart/1/edit/', {'client': 1})

        self.login({'username': 'username', 'password': 'password@123'})
        response = self.client.get('/cart/1/edit/')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        response = self.client.post('/cart/1/edit/', {'client': 1})

    def test_add_to_cart_has_count(self):
        response = self.client.get('/cart/1/add/1/2/')
        self.assertEqual(response.status_code, 404) #TODO: CHECK REDIRECT TO ERROR PAGE 404

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
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

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
        self.assertEqual(response.status_code, 404)  # TODO: CHECK REDIRECT TO ERROR PAGE 404

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
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

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
        self.assertEqual(response.status_code, 200)  # TODO: CHECK REDIRECT TO ERROR PAGE

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        category = Category.objects.create(name='c1')
        product = Product.objects.create(name='p1', category=category, price=10, description='text', photo='1')
        response = self.client.get('/product/1/')
        self.assertEqual(len(response.context['forms']), 1)

        cart_item = CartItem.objects.create(product=Product.objects.get(pk=1), count=1, cart=Cart.objects.get(pk=1))
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



        # account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
        #                                       is_staff=True)
        # self.login({'username': 'admin', 'password': 'password@123'})
        # category = Category.objects.create(name='c1')
        # product = Product.objects.create(name='p1', category=category, price=10, description='text')
        # cart = Cart.objects.create(client=Account.objects.get(pk=1))
        #
        # response = self.client.get('/cart/1/add/1/2/')
        # self.assertEqual(CartItem.objects.all().count(), 1)
        #
        # self.create_user_and_login()
        # response = self.client.get('/cart/1/add/1/2/')
        # # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        # self.assertEqual(b'You are not permitted to visit this page', response.content)
        #
        # cart = Cart.objects.create(client=Account.objects.get(pk=2))
        # response = self.client.get('/cart/2/add/1/2/')
        # self.assertEqual(CartItem.objects.all().count(), 2)
        # self.assertEqual(Cart.objects.get(pk=2).total, 20)
        #
        # cart = Cart.objects.create(client=Account.objects.get(pk=2))
        # response = self.client.get('/cart/2/add/1/2/')
        # self.assertEqual(CartItem.objects.get(pk=2).count, 4)
        #
        # self.login({'username': 'admin', 'password': 'password@123'})
        # cart = Cart.objects.create(client=Account.objects.get(pk=2))
        # response = self.client.get('/cart/2/add/1/2/')
        # self.assertEqual(CartItem.objects.get(pk=2).count, 6)