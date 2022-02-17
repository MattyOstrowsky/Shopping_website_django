from django.test import TestCase
from shop.models import Product
from .models import Customer, Employee
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


def create_group_and_permission():
    group_names = ["customer", "employee"]
    for group_name in group_names:
        group = Group.objects.get_or_create(name=group_name)

    customer_group = Group.objects.get(name="customer")
    content_type = ContentType.objects.get_for_model(Product)
    user_perm = Permission.objects.filter(content_type=content_type)
    customer_group.permissions.set(user_perm)


class TestUserAccount(TestCase):
    def setUp(self):
        if (
            not Group.objects.get(name="customer").exists()
            and not Group.objects.get(name="employee").exists()
        ):
            create_group_and_permission()

        self.customer = get_user_model().objects.create_user(
            email="jacob@sdf.com", password="top_secret", is_customer=True
        )
        self.employee = get_user_model().objects.create_user(
            email="jacob2@sdf.com", password="top_secret", is_employee=True
        )

    def test_user_profile_is_created(self):
        customer = Customer.objects.get(user=self.customer)
        employee = Employee.objects.get(user=self.employee)
        self.assertEqual(str(customer.user), self.customer.email)
        self.assertEqual(str(employee.user), self.employee.email)

    def test_user_profile_is_in_correct_group(self):
        self.assertTrue(self.customer.groups.filter(name="customer").exists())
        self.assertTrue(self.employee.groups.filter(name="employee").exists())
        self.assertFalse(self.customer.groups.filter(name="employee").exists())
        self.assertFalse(self.employee.groups.filter(name="customer").exists())

    def test_user_profile_permissions(self):
        customer_group = Group.objects.get(name="customer")

        for perm in list(self.customer.get_group_permissions()):
            self.assertTrue(
                perm[5:]
                in customer_group.permissions.all().values_list("codename", flat=True)
            )
