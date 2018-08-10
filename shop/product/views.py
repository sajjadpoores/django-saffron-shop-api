from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .forms import ProductForm, CategoryForm, AddToCartForm, DeleteFromCartForm
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
        from cart.views import get_cartid
        from cart.views import product_is_already_in_cart

        product = get_product_or_404(id)
        cart = get_cartid(request)

        forms = [AddToCartForm(initial={'pid': id, 'count': 0})]
        submits = ['اضافه به سبد']
        actions = ['/cart/' + str(cart.id) + '/add/' + str(id) + '/']
        methods = ['POST']
        if product_is_already_in_cart(cart, product, 0):
            forms.append(DeleteFromCartForm())
            submits.append('حذف از سبد')
            actions.append('/cart/' + str(cart.id) + '/delete/' + str(id) + '/')
            methods.append('GET')

        return render(request, 'product/detail.html', {'product': product, 'forms': forms, 'submits': submits,
                                                       'actions': actions, 'methods': methods})

    def add_to_cart_return_message(self, request, form, id):
        count = form.cleaned_data['count']
        from cart.views import get_cartid, AddToCart
        cart = get_cartid(request)
        message = AddToCart.get(AddToCart, request, cart.id, id, count).content
        return message

    def post(self, request, id, *args, **kwargs):
        product = get_product_or_404(id)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            message = self.add_to_cart_return_message(request, form, id)
            return render(request, 'product/detail.html', {'product': product, 'form': form, 'message': message})
        return render(request, 'product/detail.html', {'product': product, 'form': form})


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


class CategoryDetailView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        category = get_category_or_404(id)
        return render(request, 'category/detail.html', {'category': category})


class CategoryDeleteView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        if user_is_staff(request):
            category = get_category_or_404(id)
            category.delete()
            return HttpResponse('Category is deleted!') # TODO: REDIRECT USER TO HOMEPAGE
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE


class CategoryProductsView(TemplateView):

    def get(self, request, id, *args, **kwargs):
        products = Product.objects.all().filter(category=id)
        return render(request, 'product/list.html', {'products': products})