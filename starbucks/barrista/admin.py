from django.contrib import admin

from barrista.models import Product
from barrista.models import Order

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
