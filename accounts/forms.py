from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django_summernote.widgets import SummernoteWidget

from accounts.models import ProfileImage, Company


class AbstractUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Password"},
    ))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Re-Type Password"},
    ))

    class Meta:
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


class UserCreationForm(AbstractUserCreationForm, forms.Form):
    """ A form is prepared for admin users to regster. Includes all the required
        fields, plus a repeated password.
    """
    usertype = forms.ChoiceField(required=True,
                                 widget=forms.RadioSelect(
                                     attrs={'type': 'radio'}),
                                 choices=(('supplier', 'Supplier'),
                                          ('manufacture', 'Manufacturer'))
                                 )


class AdminCreateUserForm(AbstractUserCreationForm, forms.Form):
    """
    this form is created for creating users by super admin
    """
    user_roles = forms.ChoiceField(required=True,
                                   widget=forms.Select(
                                       attrs={'type': 'select', "class": "form-control form-control-uniform"}),
                                   choices=(('admin', 'Super Admin'), ('suplier', 'Supplier'), (
                                       'manufacturer', 'Manufacturer'), ('customer', 'Customer'),)
                                   )


class CompanyUserCreationForm(AbstractUserCreationForm):
    """
    this form is created for supplier and manufacturer admins for creating company users.
    """
    # user_group = forms.ChoiceField(required=True,
    #                                widget=forms.Select(
    #                                    attrs={'type': 'select', "class": "form-control form-control-uniform"}),
    #                                choices=(
    #                                    ('',"Select User Group"),
    #                                    ('comp_admin','System Admin'),
    #                                    ('store_keeper', 'Store Keeper'),
    #                                    ('it_specialist', 'It Specialist'),
    #                                    ('data_encoder', 'Data Encoder'),
    #                                    ('product_manager', 'Product Manager'),
    #                                    )
    #                                )
    class Meta(AbstractUserCreationForm.Meta):
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone_number','group_name',)
        widgets = {
            'first_name': forms.TextInput(attrs={"placeholder": "First Name", },),
            'last_name': forms.TextInput(attrs={"placeholder": "Last Name"},),
            'username': forms.TextInput(attrs={"placeholder": "User Name"},),
            'email': forms.TextInput(attrs={"placeholder": "User Email"},),
            'phone_number': forms.TextInput(attrs={"placeholder": "Phone Number", "data-mask": "+251-99999-9999"},),
        }
        

class GroupCreationForm(forms.ModelForm):
    class Meta:
        model=Group
        fields = ('__all__')
    
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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = ProfileImage
        fields = ("profile_image",)
        widgets = {
            "profile_image": forms.FileInput(attrs={'class': "form-input-styled"})
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('company_name', 'company_name_am', 'email', 'phone_number',
                  'detail', 'detail_am', 'company_logo', 'location', 'company_intro',)
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(English)'}),
            'company_name_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(Amharic)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address..'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number...', "data-mask": "+251-99999-9999"}),
            'company_logo': forms.FileInput(attrs={'class': 'form-input-styled'}),
            'company_intro': forms.FileInput(attrs={'class': 'form-input-styled'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'detail': forms.Textarea(attrs={'class': 'summernote'}),
            'detail_am': forms.Textarea(attrs={'class': 'summernote'}),
        }
