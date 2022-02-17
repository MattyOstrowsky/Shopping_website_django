from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
    ("CONFIRMATION", "Waiting for confirmation"),
    ("PENDING", "Pending"),
    ("COMPLETED", "COMPLETED"),
]


class Bucket(models.Model):
    payment_status = models.BooleanField(default=False, help_text=_("Payment status"))
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="CONFIRMATION")
    amount = models.FloatField(blank=False, null=False, help_text=_("To pay"))

    def __str__(self):
        return self.user.email

class BucketItem(models.Model):
    bucket = models.ForeignKey("stock.Bucket", on_delete=models.CASCADE)
    product  = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    units = models.IntegerField(default= 1, blank=False, null=False)
    
    def __str__(self):
        return self.product.prod_name
