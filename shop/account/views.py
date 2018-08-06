from django.http import HttpResponse
from django.shortcuts import render
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
                return HttpResponse('logged in')   # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        else:
            error = 'نام کاربری یا کلمه عبور اشتباه است.'
            return render(request, 'account/login.html', {'form': form, 'error': error})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self.get_user_or_none(form)
            return self.login_user_or_show_error(request, user, form)
        else:
            return render(request, 'account/login.html', {'form': form})


class SignupView(TemplateView):

    @staticmethod
    def check_user_login_status(request):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponse('You are logged in, cant create account.') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE

    def get(self, request, *args, **kwargs):
        self.check_user_login_status(request)
        form = SignupForm()
        return render(request, 'account/signup.html', {'form': form, 'states': states})

    def post(self, request, *args, **kwargs):
        self.check_user_login_status(request)
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('signed up')  # TODO: REDIRECT TO LOGIN PAGE
        else:
            return render(request, 'account/signup.html', {'form': form, 'states': states})


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('You have successfully logged out.')  # TODO: REDIRECT USER TO HOMEPAGE OR LOGIN PAGE?!
        return HttpResponse("You have already logged out.")  # TODO: REDIRECT TO HOMEPAGE


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

        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT USER TO HOME PAGE

    def post(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            form = self.get_account_return_form(request, id)
            if form.is_valid():
                account = form.save()
                login(request, account)
                return HttpResponse('account updated')  # TODO: REDIRECT USER TO HOME PAGE OR DETAIL PAGE?
            else:
                return render(request, 'account/edit.html', {'form': form, 'states': states})

        return HttpResponse('You are not permitted to edit this account')  # TODO: REDIRECT USER TO HOME PAGE


class DetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_permitted_to_view(request, id):
            account = get_account_or_404(id)
            return render(request, 'account/detail.html', {'account': account})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT USER TO HOME PAGE


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
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT USER TO HOME PAGE


class DeactivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if account.is_active:
                account.is_active = False
                account.save()
                return HttpResponse('Account deactivated!') # TODO: REDIRECT USER TO LAST VISITED PAGE
            return HttpResponse('Account is already deactivated!')
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT USER TO HOME PAGE


class ActivateView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if ListView.user_is_permitted_to_view_list(request):
            account = get_account_or_404(id)
            if not account.is_active:
                account.is_active = True
                account.save()
                return HttpResponse('Account activated!') # TODO: REDIRECT USER TO LAST VISITED PAGE
            return HttpResponse('Account is already activated!')  # TODO: REDIRECT USER TO LAST VISITED PAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT USER TO HOME PAGE
