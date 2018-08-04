from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from .forms import LoginForm
# Create your views here.
class LoginView(TemplateView):        

    def get_user_or_none(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        return authenticate(username=username, password=password)

    def login_user_or_show_error(self, request, user, form):
        if user is not None:
                login(request, user)
                return HttpResponse('logged in')  # TODO: REDIRECT USER TO HOME PAGE
        else:
            error = 'نام کاربری یا کلمه عبور اشتباه است.'
            return render(request, 'login.html', {'form': form, 'error': error})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in')
        
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse('User is already logged in')
        
        form = LoginForm(request.POST)
        if form.is_valid():
            user = self.get_user_or_none(form)
            return self.login_user_or_show_error(request, user, form)
        else:
            return render(request, 'login.html', {'form': form})

