from django.utils import timezone
from django.db import models
from account.models import Account
from product.models import Product


class Cart(models.Model):
    client = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='مشتری', blank=True, null=True,
                               default=None)
    create_time = models.DateTimeField(verbose_name='زمان ایجاد', blank=True, null=True)
    is_payed = models.BooleanField(verbose_name='وضعیت پرداخت', default=False, blank=False)
    total = models.PositiveIntegerField(verbose_name='مجموع', default=0, blank=True, null=False)

    def __str__(self):
        return self.client.__str__() + ' - ' + str(self.create_time)

    def save(self, *args, **kwargs):
        self.create_time = timezone.now()
        return super(Cart, self).save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='سبد خرید', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', blank=False, null=False)
    count = models.PositiveIntegerField(verbose_name='تعداد', default=1, blank=False, null=False)
    create_time = models.DateTimeField(verbose_name='زمان ایجاد', blank=False, null=False)

    def __str__(self):
        return self.card.__str__() + ' - ' + self.product.__str__()

    def save(self, *args, **kwargs):
        self.create_time = timezone.now()
        return super(CartItem, self).save(*args, **kwargs)