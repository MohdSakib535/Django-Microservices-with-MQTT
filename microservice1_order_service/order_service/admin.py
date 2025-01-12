from django.contrib import admin
from order_service.models import Order, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
