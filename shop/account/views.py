from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from .consts import states
from .models import Account
from django.shortcuts import get_object_or_404
from cart.views import get_cartid


class LoginView(TemplateView):

    @staticmethod
    def get_user_or_none(form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        return authenticate(username=username, password=password)

    @staticmethod
    def login_user_or_show_error(request, user, form):
        if user is not None:
                login(request, user)
                messages.success(request, user.first_name + ' عزیز، خوش آمدید.')
                return redirect('/home/')
        else:

            cart = get_cartid(request)

            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است.')
            return render(request, 'account/login.html', {'form': form, 'cartid': cart.id})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما قبلا وارد شده اید.')
            return redirect('/home/')
        
        form = LoginForm()

        cart = get_cartid(request)

        return render(request, 'account/login.html', {'form': form, 'cartid': cart.id})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما قبلا وارد شده اید.')
            return redirect('/home/')
        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self.get_user_or_none(form)
            return self.login_user_or_show_error(request, user, form)
        else:
            cart = get_cartid(request)

            return render(request, 'account/login.html', {'form': form, 'cartid': cart.id})


class SignupView(TemplateView):

    @staticmethod
    def user_is_loggedin(request):
        if request.user.is_authenticated and not request.user.is_staff:
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.user_is_loggedin(request):
            messages.warning(request, 'شما قبلا ثبت نام کرده اید.')
            return redirect('/home/')
        form = SignupForm()

        cart = get_cartid(request)

        return render(request, 'account/signup.html', {'form': form, 'states': states, 'cartid': cart.id})

    def post(self, request, *args, **kwargs):
        if not self.user_is_loggedin(request):
            form = SignupForm(request.POST)

            if form.is_valid():
                account = form.save()
                if not request.user.is_staff:
                    cart = get_cartid(request)
                    cart.client = account
                    cart.save()

                    login(request, account)

                    messages.success(request, account.first_name + ' عزیز، خوش آمدید.')
                    return redirect('/home/')

                messages.success(request, 'کاربر جدید ایجاد شد.')
                return redirect('/account/all/')
            else:
                cart = get_cartid(request)

                return render(request, 'account/signup.html', {'form': form, 'states': states, 'cartid': cart.id})

        messages.warning(request, 'شما قبلا ثبت نام کرده اید.')
        return redirect('/home/')


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'شما با موفقیت خارج شدید.')
            return redirect('/home/')
        messages.warning(request, 'شما وارد حساب خود نیستید.')
        return redirect('/home/')


def user_is_permitted_to_view(request, id):
    if request.user.is_authenticated and (request.user.id == id or request.user.is_staff):
        return True
    return False


def get_account_or_404(id):
    account = get_object_or_404(Account, pk=id)
    return account


class EditView(TemplateView):

    @staticmethod
    def get_account_return_form(request, id):
        account = get_account_or_404(id)
        if request.method == 'POST':
            return SignupForm(request.POST, instance=account)
        return SignupForm(instance=account)

    def get(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            form = self.get_account_return_form(request, id)

            cart = get_cartid(request)

            return render(request, 'account/edit.html', {'form': form, 'states': states, 'cartid': cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')

    def post(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            form = self.get_account_return_form(request, id)
            if form.is_valid():
                account = form.save()
                login(request, account)

                messages.success(request, 'پروفایل کاربر با موفقیت ویرایش شد.')
                return redirect('/account/' + str(id) + '/')
            else:

                cart = get_cartid(request)

                return render(request, 'account/edit.html', {'form': form, 'states': states, 'cartid': cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class DetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            account = get_account_or_404(id)
            cart = get_cartid(request)
            return render(request, 'account/detail.html', {'account': account, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class ListView(TemplateView):

    @staticmethod
    def user_is_permitted_to_view_list(request):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.user_is_permitted_to_view_list(request):
            accounts = Account.objects.all()

            cart = get_cartid(request)

            return render(request, 'account/list.html', {'accounts': accounts, 'cartid': cart.id})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class DeactivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if account.is_active:
                account.is_active = False
                account.save()
                messages.success(request, 'حساب کاربر غیر فعال شد.')
                return redirect('/account/' + str(id) + '/')
            messages.error(request, 'حساب کاربر قبلا غیر فعال شده است.')
            return redirect('/account/' + str(id) + '/')
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class ActivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if not account.is_active:
                account.is_active = True
                account.save()
                messages.success(request, 'حساب کاربر فعال شد.')
                return redirect('/account/' + str(id) + '/')
            messages.error(request, 'حساب کاربر قبلا فعال شده است.')
            return redirect('/account/' + str(id) + '/')
        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')
