from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .forms import ProductForm
from .models import Product


def user_is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    return False


class CreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm()
            return render(request, 'product/create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return HttpResponse('Product created!')

            return render(request, 'product/create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def get_product_or_404(id):
    account = get_object_or_404(Product, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return account


class EditView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            form = ProductForm(instance=product)
            return render(request, 'product/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()
                return HttpResponse('UPDATED')  # TODO: REDIRECT TO PRODUCT DETAIL

            return render(request, 'product/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class ListView(TemplateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'product/list.html', {'products': products})
