from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from stock.models import Bucket
from django.contrib.auth.models import Group


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        print ("Creating user...")
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()      
        if user.is_customer == True:
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            customer = Customer.objects.create(user=user)             
            customer.save()
        elif user.is_employee == True:
            group = Group.objects.get(name = 'employee')
            user.groups.add(group)
            employee = Employee.objects.create(user=user)
            employee.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["is_customer", "is_employee"]

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email


class Employee(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email


class Customer(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    order = models.ForeignKey(
        Bucket, on_delete=models.CASCADE, blank=True,null=True, help_text=_("Shopping cart")
    )
    country = models.CharField(
        max_length=20, null=True, blank=True, help_text=_("Country")
    )
    city = models.CharField(max_length=50, null=True, blank=True, help_text=_("City"))
    address = models.CharField(
        max_length=200, blank=True, null=True, help_text=_("Adress")
    )
    apartment = models.IntegerField(null=True, blank=True, help_text=_("Apartment"))
    zip_code = models.CharField(
        max_length=20, null=True, blank=True, help_text=_("ZIP Code")
    )

    def __str__(self):
        return self.user.email
