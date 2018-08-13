from django.db import models
from account.models import Account


class Category(models.Model):
    name = models.CharField(verbose_name='دسته', max_length=50, blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='نام محصول', max_length=50, blank=False, null=False)
    photo = models.ImageField(verbose_name='تصویر', upload_to='')
    price = models.IntegerField(verbose_name='قیمت', blank=False, null=False)
    description = models.TextField(verbose_name='توضیحات', max_length=500, blank=False, null=False)
    inventory = models.IntegerField(verbose_name='موجودی', blank=False, null=False, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته', blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'category')