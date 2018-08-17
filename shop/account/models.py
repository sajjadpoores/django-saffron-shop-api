from django.db import models
from django.contrib.auth.models import AbstractUser


class State(models.Model):
    name = models.CharField(verbose_name='استان', max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='استان', blank=False, null=False)
    name = models.CharField(verbose_name='شهر', max_length=30, blank=False, null=False)

    def __str__(self):
        return self.name


class Account(AbstractUser):
    first_name = models.CharField(verbose_name='نام', max_length=30, blank=False)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150, blank=False)
    email = models.EmailField(verbose_name='ایمیل', blank=False)
    phone = models.CharField(verbose_name="تلفن همراه",max_length=11, blank=False)
    post_code = models.CharField(verbose_name='کد پستی', max_length=10, default=0, blank=False)
    national_id = models.CharField(verbose_name="شماره ملی", max_length=10, default=0, blank=False, unique=True)

    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='استان', blank=False, default=11)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر', blank=False, default=436)
    address = models.CharField(verbose_name='آدرس', max_length=200, blank=False, default='')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone', 'national_id', 'post_code', 'address']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
