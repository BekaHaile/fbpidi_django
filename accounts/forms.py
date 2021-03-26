from django import forms 
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import (
                                        ReadOnlyPasswordHashField,
                                        UserCreationForm,
                                        AuthenticationForm,
                                        UsernameField
                                        )
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext as _
from django.contrib.admin.forms import AdminAuthenticationForm

from django_summernote.widgets import SummernoteWidget

from accounts.models import Company, CompanyAdmin, Customer
from company.models import CompanyStaff


# For the Front End Login Form
class FrontLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username',widget=forms.TextInput())

# Customized Admin Login Form
class AdminLoginForm(AdminAuthenticationForm):
    username = forms.CharField(label='Email / Username',widget=forms.TextInput(
        attrs={'placeholder':'Email / Username'}
    ))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'current-password'}),
    )

# Abstract User Sign Up Form where the other forms extend this form.
class AbstractUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Re-Type Password"},
    ))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
 


class CompanyAdminCreationForm(AbstractUserCreationForm):
    """ A form is prepared for admin users to regster. Includes all the required
        fields, plus a repeated password.
    """
    designation = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Responsiblity'}
    ))
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company_admin = True
        user.is_staff = True
        user.is_superuser = False
        user.is_active = False
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        admin_permisstion_list = Permission.objects.all().exclude(
            codename__in=['add_logentry','change_logentry','delete_logentry','view_logentry',
                          'add_permission','change_permission','delete_permission','view_permission',
                          'add_group','change_group','delete_group','view_group',
                          'add_contenttype','change_contenttype','delete_contenttype','view_contenttype',
                          'add_session','change_session','delete_session','view_session'] 
            )
        
        user.user_permissions.set(admin_permisstion_list)
        user.save()
        comp_admin = CompanyAdmin.objects.create(user=user,designation=self.cleaned_data.get('designation'))
        return user


class CustomerCreationForm(AbstractUserCreationForm):
    """ A form is prepared for normal/customer users to regster. Includes all the required
        fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={},
    ))

    class Meta(AbstractUserCreationForm.Meta):
        widgets = {
            'first_name': forms.TextInput(attrs={},),
            'last_name': forms.TextInput(attrs={},),
            'username': forms.TextInput(attrs={},),
            'email': forms.TextInput(attrs={},),
            'phone_number': forms.TextInput(attrs={},),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.is_customer = True
        user.is_active = False
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        customer = Customer.objects.create(user=user)
        customer.save()
        return user


class AdminCreateUserForm(AbstractUserCreationForm):
    """
    This form is for creating users by super admins
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Create Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-Type Password'},
    ))
    user_type = forms.ChoiceField(required=True,
                                  widget=forms.Select(
                                      attrs={'type': 'select', "class": "form-control form-control-uniform"}),
                                  choices=(('', 'Select User Types'),
                                            ('admin', 'Super Admin'),
                                            ('contact_person', 'Company Contact Person'),
                                            ('customer', 'Customer'),)
                                  )
    designation = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Responsiblity'}
    ))
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if self.cleaned_data.get("user_type") == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()
        if self.cleaned_data.get("user_type") == "contact_person":
            user.is_company_admin = True
            user.is_staff = True
            user.save()
            admin_permisstion_list = Permission.objects.all().exclude(
            codename__in=['add_logentry','change_logentry','delete_logentry','view_logentry',
                          'add_permission','change_permission','delete_permission','view_permission',
                          'add_group','change_group','delete_group','view_group',
                          'add_contenttype','change_contenttype','delete_contenttype','view_contenttype',
                          'add_session','change_session','delete_session','view_session'] 
            )
            user.user_permissions.set(admin_permisstion_list)
            user.save()
            comp_admin = CompanyAdmin.objects.create(user=user,designation=self.cleaned_data.get('designation'))
            comp_admin.save()
        elif self.cleaned_data.get("user_type") == "customer":
            user.is_customer = True
            user.save()
            comp_admin = Customer.objects.create(user=user)
            comp_admin.save()
        return user


class CompanyUserCreationForm(AbstractUserCreationForm):
    """
    this form is for industry admins for creating company users.
    """
    
    user_type = forms.ModelChoiceField(
        empty_label="Select User Role",
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={}),
        required=True
    )

    class Meta(AbstractUserCreationForm.Meta):
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone_number',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_company_staff = True
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        user.groups.add(Group.objects.get_by_natural_key(
            self.cleaned_data.get("user_type")))
        return user


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('__all__')
        widgets = {
            'permissions': forms.Select(attrs={'class': 'form-control listbox', 'multiple': "multiple"})
        }

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        return group


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password',)
        widgets = {
            'email': forms.EmailInput(
                attrs={}
            )
        }

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


 