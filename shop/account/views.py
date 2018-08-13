from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from .consts import states
from .models import Account
from django.shortcuts import get_object_or_404


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
            error = 'نام کاربری یا کلمه عبور اشتباه است.'
            return render(request, 'account/login.html', {'form': form, 'error': error})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما قبلا وارد شده اید')
            return redirect('/home/')
        
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'شما قبلا وارد شده اید')
            return redirect('/home/')
        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self.get_user_or_none(form)
            return self.login_user_or_show_error(request, user, form)
        else:
            return render(request, 'account/login.html', {'form': form})


class SignupView(TemplateView):

    @staticmethod
    def user_is_loggedin(request):
        if request.user.is_authenticated and not request.user.is_staff:
            return True
        return False

    def get(self, request, *args, **kwargs):
        if self.user_is_loggedin(request):
            messages.warning(request, 'شما وارد شده اید.')
            return redirect('/home/')
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form, 'states': states})

    def post(self, request, *args, **kwargs):
        self.check_user_login_status(request)
        form = SignupForm(request.POST)

        if form.is_valid():
            account = form.save()
            from cart.views import get_cartid
            if not request.user.is_staff:
                cart = get_cartid(request)
                cart.client = account
                cart.save()

                login(request, account)

            messages.success(request, account.first_name + ' عزیز، خوش آمدید.')
            return redirect('/home/')
        else:
            return render(request, 'account/signup.html', {'form': form, 'states': states})


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
    return account # TODO: REDIRECT TO ERROR PAGE


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
            return render(request, 'account/edit.html', {'form': form, 'states': states})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
        return redirect('/home/')

    def post(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            form = self.get_account_return_form(request, id)
            if form.is_valid():
                account = form.save()
                login(request, account)
                return HttpResponse('account updated')  # TODO: REDIRECT USER TO DETAIL PAGE
            else:
                return render(request, 'account/edit.html', {'form': form, 'states': states})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
        return redirect('/home/')


class DetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            account = get_account_or_404(id)
            return render(request, 'account/detail.html', {'account': account})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
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
            return render(request, 'account/list.html', {'accounts': accounts})
        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
        return redirect('/home/')


class DeactivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if account.is_active:
                account.is_active = False
                account.save()
                return HttpResponse('Account deactivated!') # TODO: REDIRECT USER TO LAST VISITED PAGE
            return HttpResponse('Account is already deactivated!')
        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
        return redirect('/home/')


class ActivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if not account.is_active:
                account.is_active = True
                account.save()
                return HttpResponse('Account activated!') # TODO: REDIRECT USER TO LAST VISITED PAGE
            return HttpResponse('Account is already activated!')  # TODO: REDIRECT USER TO LAST VISITED PAGE
        messages.error(request, 'دسترسی به این صفحه مجاز نیست')
        return redirect('/home/')
