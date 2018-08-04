from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری', max_length=150)
    password = forms.CharField(label='کلمه عبور', max_length=150, widget=forms.PasswordInput)