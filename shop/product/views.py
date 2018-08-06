from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from .forms import ProductForm


def user_is_staff(request):
    if request.user.is_authenticated and request.user.is_staff:
        return True
    return False


class CreateView(TemplateView):

    def get(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm()
            return render(request, 'create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE

    def post(self, request, *args, **kwargs):
        if user_is_staff(request):
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return HttpResponse('Product created!')

            return render(request, 'create.html', {'form': form})
        return HttpResponse('You are not permitted to visit this page')  # TODO: REDIRECT TO HOMEPAGE
