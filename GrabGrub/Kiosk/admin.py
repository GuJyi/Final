from django.contrib import admin
from .models import User, Food, Customer, Order
admin.site.register(User)
admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Order)
# Register your models here.
