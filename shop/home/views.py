from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        from cart.views import  get_cartid
        cart = get_cartid(request)
        return render(request, 'home/home.html', {'cartid': cart.id})


class AdminView(TemplateView):

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            from cart.views import get_cartid
            cart = get_cartid(request)
            return render(request, 'home/admin.html', {'cartid': cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


class DashboardView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from cart.views import get_cartid
            cart = get_cartid(request)
            return render(request, 'home/dashboard.html', {'cartid': cart.id})

        messages.error(request, 'دسترسی به این صفحه مجاز نیست.')
        return redirect('/home/')


def handler404(request, exception, template_name='404.html'):
    messages.error(request, 'صفحه مورد نظر پیدا نشد.')
    return redirect('/home/')