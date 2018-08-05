from django.test import TestCase
from account.forms import LoginForm, SignupForm
from account.models import Account, State, City
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
    def test_login_view(self):
        # GET TESTS
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/account/login')
        self.assertEqual(response.status_code, 301)

        # POST TESTS
        # TODO: WRITE SIGNUP VIEW AND IT"S TEST THEN WRITE POST RELATED TESTS
        