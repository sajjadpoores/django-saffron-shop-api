from django.forms.models import ModelForm
from .models import Cart


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['client', 'create_time', 'is_payed', 'total']