from django.test import TestCase
from .forms import ProductForm, CategoryForm
from .models import Category, Product
from account.models import Account, State, City
from cart.models import Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages
from random import randint


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

    def test_category_create_form_validation(self):
        post_data = {'name': ''}
        form = CategoryForm(data=post_data)
        self.assertFalse(form.is_valid())
        post_data = {'name': 'cat1'}
        form = CategoryForm(data=post_data)
        self.assertTrue(form.is_valid())

        post_data = {'name': 1}
        form = CategoryForm(data=post_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Category.objects.get(pk=1).name, '1')


class ViewTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name='cat1')
        state = State.objects.create(name='خراسان رضوی')
        city = City.objects.create(name='مشهد', state=state)

    def login(self, login_data={'username': 'username', 'password': 'password@123'}):
        response = self.client.get('/account/logout/')

        response = self.client.post('/account/login/', login_data)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue('عزیز، خوش آمدید' in str(messages[len(messages)-1]))

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
        response = self.client.get('/product/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

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
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

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

        account = Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123',
                                              is_staff=True)
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

        self.assertEqual(len(response.context['forms']), 1)
        from cart.views import get_cartid
        request = response.wsgi_request
        cartid = get_cartid(request).id
        cart_item = CartItem.objects.create(product=Product.objects.get(pk=1), count=1,
                                            cart=Cart.objects.get(pk=cartid))

        response = self.client.get('/product/1/')
        self.assertTemplateUsed(response, 'product/detail.html')
        self.assertEqual(len(response.context['forms']), 2)

    def test_delete_view(self):
        response = self.client.get('/product/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/1/delete/')
        #TODO: CHECK 404 NOT FOUND PAGE

        photo_file = open('product/test_pic.jpg', 'rb')
        post_data = {'name': 'product1', 'price': '12000', 'description': 'qweqwe', 'inventory': '111', 'category': '1',
                     'photo': SimpleUploadedFile(photo_file.name, photo_file.read())}
        self.client.post('/product/create/', post_data)
        self.assertEqual(Product.objects.all().count(), 1)
        photo_file.close()

        response = self.client.get('/product/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'محصول با موفقیت حذف شد.')

    def test_create_category_view(self):
        response = self.client.get('/product/category/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/category/create/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/category/create/')
        self.assertTemplateUsed(response, 'category/create.html')

        post_data = {'name': 'cat2'}
        response = self.client.post('/product/category/create/', post_data)
        self.assertEqual(Category.objects.get(pk=2).name, 'cat2')

        response = self.client.post('/product/category/create/')
        self.assertTrue(b'field is required', response.context['form'].errors)

    def test_edit_category_view(self):
        response = self.client.get('/product/category/100/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/category/1/edit/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/category/1/edit/')
        self.assertTemplateUsed(response, 'category/edit.html')

        post_data = {'name': 'first_category'}
        response = self.client.post('/product/category/1/edit/', post_data)
        self.assertEqual(Category.objects.get(pk=1).name, 'first_category')

        response = self.client.get('/product/category/2/edit/')
        self.assertTemplateNotUsed(response, 'category/edit.html') #TODO: CHECK REDIRECTION TO ERROR PAGE 404

    def test_category_list_view(self):
        response = self.client.get('/product/category/all/')
        self.assertTemplateUsed(response, 'category/list.html')

        self.create_user_and_login()
        response = self.client.get('/product/category/all/')
        self.assertTemplateUsed(response, 'category/list.html')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})
        response = self.client.get('/product/category/all/')
        self.assertTemplateUsed(response, 'category/list.html')

    def test_category_detail_view(self):
        response = self.client.get('/product/category/1/')
        self.assertTemplateUsed(response, 'category/detail.html')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/category/1/')
        self.assertTemplateUsed(response, 'category/detail.html')

        self.create_user_and_login()
        response = self.client.get('/product/category/1/')
        self.assertTemplateUsed(response, 'category/detail.html')

        response = self.client.get('/product/category/2/')
        self.assertTemplateNotUsed(response, 'category/detail.html') #TODO: CHECK REDIRECTION TO ERROR PAGE

    def test_category_delete_view(self):
        response = self.client.get('/product/category/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        self.create_user_and_login()
        response = self.client.get('/product/category/1/delete/')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[len(messages) - 1]), 'دسترسی به این صفحه مجاز نیست.')

        Account.objects.create_user(username='admin', email='admin@admin.com', password='password@123', is_staff=True)
        self.login({'username': 'admin', 'password': 'password@123'})

        response = self.client.get('/product/2/category/delete/')
        # TODO: CHECK 404 NOT FOUND PAGE

        response = self.client.get('/product/category/1/delete/')
        self.assertEqual(Category.objects.all().count(), 0)

    def test_search_view(self):
        category = Category.objects.get(pk=1)
        p1 = Product.objects.create(name='p1', category=category, price=10, description='text')
        p2 = Product.objects.create(name='p2', category=category, price=10, description='text')
        p1.save()
        p2.save()
        response = self.client.get('/product/p/search/')
        self.assertEqual(response.context['products'].count(), 2)

        response = self.client.get('/product/1/search/')
        self.assertEqual(response.context['products'].count(), 1)

    def test_search_in_category_view(self):
        category = Category.objects.get(pk=1)
        Product.objects.create(name='p1', category=category, price=10, description='text')
        Product.objects.create(name='p2', category=category, price=10, description='text')

        category = Category.objects.create(name='cat2')
        Product.objects.create(name='p3', category=category, price=10, description='text')
        Product.objects.create(name='p4', category=category, price=10, description='text')

        response = self.client.get('/product/1/p/search/')
        self.assertEqual(response.context['products'].count(), 2)

        response = self.client.get('/product/2/p/search/')
        self.assertEqual(response.context['products'].count(), 2)

        response = self.client.get('/product/2/3/search/')
        self.assertEqual(response.context['products'].count(), 1)