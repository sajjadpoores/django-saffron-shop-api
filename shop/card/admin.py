from django.contrib import admin
from .models import Card, CardItem
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Card, CardAdmin)

class CardItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(CardItem, CardItemAdmin)