from django.contrib import admin
from .models import Customer, Employee, UserAccount
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'is_customer', 'is_employee', 'is_staff', 'is_superuser',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.save()
        if self.cleaned_data["is_customer"] == True:
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            customer = Customer.objects.create(user=user)             
            customer.save()
        elif self.cleaned_data["is_employee"] == True:
            group = Group.objects.get(name = 'employee')
            user.groups.add(group)
            employee = Employee.objects.create(user=user)
            employee.save()

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserAccount
        fields = ('email', 'is_customer', 'is_employee', 'is_staff', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_customer', 'is_employee', 'is_staff', 'is_superuser',)
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser','is_customer', 'is_employee', 'password')}),
        #('Personal info', {'fields': ('name', 'phone', 'date_of_birth', 'picture')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser','is_customer', 'is_employee', 'password1', 'password2')}),
        #('Personal info', {'fields': ('name', 'phone', 'date_of_birth', 'picture')}),
        # ('Groups', {'fields': ('groups',)}),
        # ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(UserAccount, AccountAdmin)
admin.site.register(Employee)
admin.site.register(Customer)