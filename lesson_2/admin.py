from django.contrib import admin
from .models import User, Order, Product



admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)