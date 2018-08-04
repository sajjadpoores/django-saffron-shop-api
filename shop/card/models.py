from django.db import models
from account.models import Account
from product.models import Product


class Card(models.Model):
    client = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='مشتری', blank=False, null=False)
    last_update = models.DateTimeField(verbose_name='آخرین آپدیت', blank=False, null=False, auto_now=True)
    is_payed = models.BooleanField(verbose_name='وضعیت پرداخت', default=False, blank=False)
    total = models.PositiveIntegerField(verbose_name='مجموع', default=0, blank=False, null=False)

    def __str__(self):
        return self.client.__str__() + ' - ' + str(self.last_update)


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, verbose_name='سبد خرید', blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', blank=False, null=False)
    count = models.PositiveIntegerField(verbose_name='تعداد', default=1, blank=False, null=False)
    create_time = models.DateTimeField(verbose_name='زمان ایجاد', blank=False, null=False, auto_now=True)

    def __str__(self):
        return self.card.__str__() + ' - ' + self.product.__str__()
