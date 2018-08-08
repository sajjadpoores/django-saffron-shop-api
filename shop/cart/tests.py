from django.utils import timezone
from django.test import TestCase
from .forms import CartForm
from .models import Cart
from account.models import State, City, Account
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