from django.contrib import admin

from stock.models import Bucket, BucketItem

# Register your models here.

admin.site.register(Bucket)
admin.site.register(BucketItem)