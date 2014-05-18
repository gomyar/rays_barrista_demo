from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)

    def __unicode__(self):
        return "<Product %s - %s>" % (self.product_id, self.name)


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "<Order %s for %s>" % (self.product.product_id,
            self.customer_name)

    @property
    def order_id(self):
        return str(self._id) if hasattr(self, "_id") else str(self.id)
