from django.test import TestCase
from .forms import ProductForm
from .models import Category, Product
from account.models import Account, State, City
from django.core.files.uploadedfile import SimpleUploadedFile


class FormTest(TestCase):

    def test_create_form_validation(self):
        category = Category.objects.create(name='cat1')
        post_data = {'name': 'product1','price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1'}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertTrue(form.is_valid())
        photo_file.close()

        post_data = {'name': 'product1', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1'}
        form = ProductForm(post_data)
        self.assertFalse(form.is_valid())

        post_data = {'name': 1, 'price': 12000, 'description': 1, 'inventory': 1, 'category': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertTrue(form.is_valid())
        photo_file.close()

        post_data = {'price': 12000, 'description': 1, 'inventory': 1, 'category': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        photo_file.close()

        post_data = {'name': 1, 'description': 1, 'inventory': 1, 'category': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        photo_file.close()

        post_data = {'name': 1, 'price': 12000, 'inventory': 1, 'category': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        photo_file.close()

        post_data = {'name': 1, 'price': 12000, 'description': 1, 'category': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        photo_file.close()

        post_data = {'name': 1, 'price': 12000, 'description': 1, 'inventory': 1}
        photo_file = open('product/test_pic.jpg', 'rb')
        file_data = {'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        form = ProductForm(post_data, file_data)
        self.assertFalse(form.is_valid())
        photo_file.close()


class ViewTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name='cat1')
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
        response = self.client.get('/product/create/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/product/create/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/create/')
        self.assertTemplateUsed('product/create.html')

        photo_file = open('product/test_pic.jpg', 'rb')
        post_data = {'name': 'product1', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1',
                     'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        response = self.client.post('/product/create/', post_data)
        self.assertEqual(Product.objects.all().count(), 1)
        photo_file.close()

    def test_edit_view(self):
        response = self.client.get('/product/1/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        self.create_user_and_login()
        response = self.client.get('/product/1/edit/')
        # TODO: CHECK STATUS CODE BEING REDIRECT WHEN HOME PAGE IS CREATED
        self.assertEqual(b'You are not permitted to visit this page', response.content)

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/1/edit/')
        self.assertTemplateNotUsed(response, 'product/edit.html')

        photo_file = open('product/test_pic.jpg', 'rb')
        post_data = {'name': 'product1', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1',
                     'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        response = self.client.post('/product/create/', post_data)
        self.assertEqual(Product.objects.all().count(), 1)

        response = self.client.get('/product/1/edit/')
        self.assertTemplateUsed(response, 'product/edit.html')
        photo_file.close()

        post_data = {'name': 'product4'}
        response = self.client.post('/product/1/edit/', post_data)
        self.assertEqual(Product.objects.get(pk=1).name, 'product1')

        post_data = {'name': 'product2', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1'}
        response = self.client.post('/product/1/edit/', post_data)
        self.assertEqual(Product.objects.get(pk=1).name, 'product2')

        post_data = {'name': 'product3', 'price': '12000', 'description': 'qweqwe', 'inventory': '111'}
        response = self.client.post('/product/1/edit/', post_data)
        self.assertEqual(Product.objects.get(pk=1).name, 'product2')

    def test_list_view(self):
        response = self.client.get('/product/all/')
        self.assertTemplateUsed(response, 'product/list.html')

        self.create_user_and_login()
        response = self.client.get('/product/all/')
        self.assertTemplateUsed(response, 'product/list.html')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/product/all/')
        self.assertTemplateUsed(response, 'product/list.html')

    def test_detail_view(self):
        response = self.client.get('/product/1/')
        self.assertTemplateNotUsed(response, 'product/detail.html')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        photo_file = open('product/test_pic.jpg', 'rb')
        post_data = {'name': 'product1', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1',
                     'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        self.client.post('/product/create/', post_data)
        self.assertEqual(Product.objects.all().count(), 1)

        response = self.client.get('/product/1/')
        self.assertTemplateUsed(response, 'product/detail.html')

        self.create_user_and_login()
        response = self.client.get('/product/1/')
        self.assertTemplateUsed(response, 'product/detail.html')