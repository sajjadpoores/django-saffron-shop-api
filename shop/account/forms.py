import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=150)
    password = forms.CharField(label='کلمه عبور', max_length=150, widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    class Meta:
            fields = ['first_name', 'last_name', 'national_id', 'email', 'phone', 'username', 'post_code', 'state',
                      'city', 'address']
            model = Account

    error_messages = {
        'password_mismatch': "کلمه عبور و تاییدیه یکسان نیستند.",
    }
    password1 = forms.CharField(
        label="کلمه عبور",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="تایید کلمه عبور",
        widget=forms.PasswordInput,
        strip=False,
    )

    username = forms.CharField(
        label='نام کاربری',
        max_length=150,
        strip=False,
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_pattern = re.compile("09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}")
        if not phone_pattern.match(phone):
            raise forms.ValidationError(
                'شماره موبایل صحیح نمی باشد ، مثال 09121234567',
                code='wrong_phone_number',
            )
        return phone

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        national_pattern = re.compile("[0-9]{10}")
        if not national_pattern.match(national_id):
            raise forms.ValidationError(
                'کدملی باید ۱۰ رقمی باشد',
                code='wrong_national_id',
            )
        return national_id

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        post_pattern = re.compile("[0-9]{10}")
        if not post_pattern.match(post_code):
            raise forms.ValidationError(
                'کد پستی باید ۱۰ رقمی باشد',
                code='wrong_national_id',
            )
        return post_code