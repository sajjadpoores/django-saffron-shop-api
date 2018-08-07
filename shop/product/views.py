from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .forms import ProductForm, CategoryForm
from .models import Product, Category


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
    product = get_object_or_404(Product, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return product


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
                return HttpResponse('product is updated')  # TODO: REDIRECT TO PRODUCT DETAIL

            return render(request, 'product/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class ListView(TemplateView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'product/list.html', {'products': products})


class DetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        product = get_product_or_404(id)
        return render(request, 'product/detail.html', {'product': product})


class DeleteView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            product = get_product_or_404(id)
            product.delete()
            return HttpResponse('Product is deleted!') # TODO: REDIRECT USER TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class CategoryCreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CategoryForm()
            return render(request, 'category/create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Category created!') # TODO: REDIRECT TO CATEGORY CREATE PAGE!
            return render(request, 'category/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


def get_category_or_404(id):
    category = get_object_or_404(Category, pk=id) # TODO: REDITRECT TO ERROR PAGE
    return category


class CategoryEditView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            form = CategoryForm(instance=category)
            return render(request, 'category/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return HttpResponse('Category edited!')  # TODO: REDIRECT TO CATEGORY CREATE PAGE!
            return render(request, 'category/edit.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class CategoryListView(TemplateView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'category/list.html', {'categories': categories})