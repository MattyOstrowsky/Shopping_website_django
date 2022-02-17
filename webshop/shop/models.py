from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    prod_name = models.CharField(max_length=200,null=False, blank=False, help_text=_("Product name"))
    price = models.FloatField(null=False, blank=False, help_text=_("Price"))
    desc = models.TextField(help_text=_("Description"))
    img = models.ImageField(blank=True,null=True, help_text=_("Product image"))
    units = models.IntegerField(blank=False, help_text=_("quantity"))
    def __str__(self):
        return self.prod_name