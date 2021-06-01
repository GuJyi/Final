from django.contrib import admin
from .models import Account, Food, Customer, Order
admin.site.register(Account)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Order)
# Register your models here.
