from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from .consts import states

class LoginView(TemplateView):

    def get_user_or_none(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        return authenticate(username=username, password=password)

    def login_user_or_show_error(self, request, user, form):
        if user is not None:
                login(request, user)
                return HttpResponse('logged in')  # # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        else:
            error = 'نام کاربری یا کلمه عبور اشتباه است.'
            return render(request, 'login.html', {'form': form, 'error': error})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE
        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self.get_user_or_none(form)
            return self.login_user_or_show_error(request, user, form)
        else:
            return render(request, 'login.html', {'form': form})


class SignupView(TemplateView):
    def check_user_login_status(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            return HttpResponse('You are logged in, cant create account.') # TODO: SHOW MESSAGE AND REDIRECT TO HOMEPAGE

    def get(self, request, *args, **kwargs):
        self.check_user_login_status(request)
        form = SignupForm()
        return render(request, 'signup.html', {'form': form, 'states': states})

    def post(self, request, *args, **kwargs):
        self.check_user_login_status(request)
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('signed up')  # TODO: REDIRECT TO LOGIN PAGE
        else:
            return render(request, 'signup.html', {'form': form, 'states': states})


class LogoutView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('You have successfully logged out.')  # TODO: REDIRECT USER TO HOMEPAGE OR LOGIN PAGE?!
        return HttpResponse("You have already logged out.")  # TODO: REDIRECT TO HOMEPAGE

