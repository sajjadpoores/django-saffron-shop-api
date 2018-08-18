from django.test import TestCase
from account.forms import LoginForm, SignupForm
from account.models import Account, State, City
from django.contrib.messages import get_messages
from random import randint


class FormTest(TestCase):
    def test_login_form_validation(self):
        login_data = {'username': 'admin', 'password': 'admin'}
        form = LoginForm(data=login_data)
        self.assertTrue(form.is_valid())

        login_data = {'username': '', 'password': 'admin'}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), False)

        login_data = {'username': 'admin', 'password': ''}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), False)

        login_data = {'username': 123, 'password': 123}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), True)

        login_data = {'username': [1,'admin',3], 'password': {'name':'admin'}}
        form = LoginForm(data=login_data)
        self.assertEqual(form.is_valid(), True)

    def test_signup_form_validation(self):
        state = State.objects.create(name='خراسان رضوی')
        city = City.objects.create(name='مشهد', state=state)

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertTrue(form.is_valid())

        signup_data = {'first_name': 1, 'last_name': 1, 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 1,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertTrue(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '072050049',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '0911234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '012346789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '2', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '2', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@12'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': 'username',
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': '123abc', 'password2': '123abc'}
        form = SignupForm(data=signup_data)
        self.assertFalse(form.is_valid())


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

    def test_signup_view(self, username='username'):
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

        response = self.client.get('/account/signup')
        self.assertEqual(response.status_code, 301)

        signup_data = {'first_name': 'first name', 'last_name': 'last name', 'national_id': '0720500494',
                       'email': 'email@emailserver.domain', 'phone': '09121234567', 'username': username,
                       'post_code': '0123456789', 'state': '1', 'city': '1', 'address': 'the address',
                       'password1': 'password@123', 'password2': 'password@123'}
        account_count = Account.objects.count()
        response = self.client.post('/account/signup/', signup_data)
        self.assertTrue(account_count+1, Account.objects.count())

        account = Account.objects.get(username='username')
        self.client.force_login(account)
        response = self.client.get('/account/signup/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED

        response = self.client.post('/account/signup/', signup_data)
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED

        self.client.logout()

    def test_login_view(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 301)

        login_data = self.create_user_and_login()

        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما قبلا وارد شده اید.')

        response = self.client.post('/account/login/', login_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما قبلا وارد شده اید.')

    def test_logout_view(self):
        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما وارد حساب خود نیستید.')

        login_data = self.create_user_and_login()

        response = self.client.post('/account/login/', login_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما قبلا وارد شده اید.')

        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما با موفقیت خارج شدید.')

        response = self.client.get('/account/logout/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'شما وارد حساب خود نیستید.')

    def test_edit_view(self):
        response = self.client.get('/account/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()

        response = self.client.get('/account/1/edit/')
        self.assertTemplateUsed(response, 'account/edit.html')
        self.assertEqual(response.context['form'].instance.username, 'username')

        response = self.client.get('/account/2/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login('username2')

        response = self.client.get('/account/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        response = self.client.get('/account/2/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertTemplateUsed(response, 'account/edit.html')
        self.assertEqual(response.context['form'].instance.username, 'username2')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/1/edit/')
        self.assertTemplateUsed(response, 'account/edit.html')

        response = self.client.get('/account/3/edit/')
        self.assertTemplateUsed(response, 'account/edit.html')

    def test_detail_view(self):
        response = self.client.get('/account/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/account/1/')
        self.assertTemplateUsed(response, 'account/detail.html')
        self.assertEqual('username', response.context['account'].username)

        self.create_user_and_login('username2')

        response = self.client.get('/account/2/')
        self.assertTemplateUsed(response, 'account/detail.html')
        self.assertEqual('username2', response.context['account'].username)

        response = self.client.get('/account/1/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/3/')
        self.assertTemplateUsed(response, 'account/detail.html')
        self.assertEqual('admin', response.context['account'].username)

        response = self.client.get('/account/1/')
        self.assertTemplateUsed(response, 'account/detail.html')
        self.assertEqual('username', response.context['account'].username)

        response = self.client.get('/account/4/') # TODO: CHECK REDIRECTION WHEN ERROR PAGE CREATED
        self.assertTemplateNotUsed(response, 'account/detail.html')

    def test_list_view(self):
        response = self.client.get('/account/all/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/account/all/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/all/')
        self.assertTemplateUsed(response, 'account/list.html')
        self.assertEqual(Account.objects.get(pk=1), response.context['accounts'][0])
        self.assertEqual(Account.objects.get(pk=2), response.context['accounts'][1])

    def test_deactivate(self):
        response = self.client.get('/account/1/deactivate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/account/1/deactivate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login('username2')
        response = self.client.get('/account/1/deactivate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/2/deactivate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'حساب کاربر غیر فعال شد.')

        response = self.client.get('/account/2/deactivate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'حساب کاربر قبلا غیر فعال شده است.')

    def test_activate(self):
        response = self.client.get('/account/1/activate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/account/1/activate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login('username2')
        response = self.client.get('/account/1/activate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/account/2/activate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'حساب کاربر قبلا فعال شده است.')

        self.client.get('/account/2/deactivate/')
        response = self.client.get('/account/2/activate/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'حساب کاربر فعال شد.')

