from django.test import TestCase
from account.forms import LoginForm
from account.models import Account
# Create your tests here.
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


class ViewTest(TestCase):
    def test_login_view(self):
        # GET TESTS
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 301)

        # POST TESTS
        # TODO: WRITE SIGNUP VIEW AND IT"S TEST THEN WRITE POST RELATED TESTS
        