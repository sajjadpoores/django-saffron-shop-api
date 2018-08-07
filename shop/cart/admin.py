from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Cart, CardAdmin)

class CardItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CartItem, CardItemAdmin)