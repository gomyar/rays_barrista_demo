from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)


# Create your models here.
class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product)
