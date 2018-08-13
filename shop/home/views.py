from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.messages import get_messages


class HomeView(TemplateView):

    def get(self, request, *args, **kwargs):
        from cart.views import  get_cartid
        cart = get_cartid(request)
        return render(request, 'home/home.html', {'cartid': cart.id})
