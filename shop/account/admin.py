from django.contrib import admin
from .models import State, City, Account
# Register your models here.

class StateAdmin(admin.ModelAdmin):
    pass
admin.site.register(State, StateAdmin)

class CityAdmin(admin.ModelAdmin):
    pass
admin.site.register(City, CityAdmin)

class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)