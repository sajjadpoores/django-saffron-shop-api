from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'inventory', 'category', 'photo']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class AddToCartForm(forms.Form):
    count = forms.IntegerField(label='تعداد', initial=1, min_value=1)


class DeleteFromCartForm(forms.Form):
    pass