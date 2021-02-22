from django import forms 
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django_summernote.widgets import SummernoteWidget

from accounts.models import Company, CompanyAdmin, Customer
from company.models import CompanyStaff

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


ADMIN_PERMISSION_LIST = [
    'add_logentry',
    'view_logentry',
    'view_permission',
    'view_group',
    'view_contenttype',
    'view_session',
    'view_category',
    'add_product',
    'change_product',
    'delete_product',
    'view_product',
    'view_subcategory',
    'add_productprice',
    'change_productprice',
    'delete_productprice',
    'view_productprice',
    'add_user',
    'change_user',
    'delete_user',
    'view_user',
    'add_companyadmin',
    'change_companyadmin',
    'delete_companyadmin',
    'view_companyadmin',
    'change_company',
    'delete_company',
    'view_company',
    'add_companystaff',
    'change_companystaff',
    'delete_companystaff',
    'view_companystaff',
    'view_failedloginlog',
    'view_loginlog',
    'view_loginattempt',
    'view_userdeactivation', 

    'add_pollsquestion',
    'view_pollsquestion',
    'change_pollsquestion',
    'delete_pollsquestion',
    'add_choices',
    'view_choices',
    'change_choices',
    'delete_choices',
    
    'view_bank',
    'add_tender',
    'view_tender',
    'change_tender',
    'delete_tender',

    'add_companybankaccount',
    'change_companybankaccount',
    'delete_companybankaccount',
    'view_companybankaccount',
    'view_tenderapplicant',

    'add_news', 
    'view_news', 
    'change_news', 
    'delete_news',

    'add_newsimages', 
    'view_newsimages', 
    'change_newsimages', 
    'delete_newsimages', 

    'add_companyevent', 
    'view_companyevent', 
    'change_companyevent', 
    'delete_companyevent', 

    'add_companyevent', 
    'view_companyevent', 
    'change_companyevent', 
    'delete_companyevent', 

    
    'add_blog', 
    'view_blog', 
    'change_blog', 
    'delete_blog', 

    'add_blogcomment', 
    'view_blogcomment', 
    'change_blogcomment', 
    'delete_blogcomment',

    'add_jobapplication', 
    'view_jobapplication', 
    'change_jobapplication', 
    'delete_jobapplication', 

    'add_vacancy', 
    'view_vacancy', 
    'change_vacancy', 
    'delete_vacancy', 

    'add_jobcategory', 
    'view_jobcategory', 
    'change_jobcategory', 
    'delete_jobcategory', 

    'add_announcement', 
    'view_announcement', 
    'change_announcement', 
    'delete_announcement', 

    'add_announcementimages', 
    'view_announcementimages', 
    'change_announcementimages', 
    'delete_announcementimages', 

    'add_researchprojectcategory', 
    'view_researchprojectcategory', 
    'change_researchprojectcategory', 
    'delete_researchprojectcategory', 

    'add_research', 
    'view_research', 
    'change_research', 
    'delete_research', 

    'add_project', 
    'view_project', 
    'change_project', 
    'delete_project', 
    
    'add_document',
    'view_document', 
    'change_document',
    'delete_document',
]


'''
Blog
BlogComment
Faqs
JobCategoty
Vacancy
JobApplication
ForumQuestion-
ForumComments
CommentReplay
Announcement-
AnnouncementImages-
ResearchProjectCategory
Research
Project
'''

class CompanyAdminCreationForm(AbstractUserCreationForm):
    """ A form is prepared for admin users to regster. Includes all the required
        fields, plus a repeated password.
    """
    usertype = forms.ChoiceField(required=True,
                                 widget=forms.RadioSelect(
                                     attrs={'type': 'radio'}),
                                 choices=(('suplier', 'Supplier'),
                                          ('manufacture', 'Manufacturer'))
                                 )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company_admin = True
        user.is_staff = True
        user.is_superuser = False
        user.set_password(self.cleaned_data.get("password1"))
        user.save()
        perm_list = []
        for code_name in ADMIN_PERMISSION_LIST:
            
            perm_list.append(Permission.objects.get(codename=code_name))
        user.user_permissions.set(perm_list)
        
        comp_admin = CompanyAdmin.objects.create(user=user)
        if self.cleaned_data.get("usertype") == "suplier":
            comp_admin.is_suplier = True
        elif self.cleaned_data.get("usertype") == "manufacture":
            comp_admin.is_manufacturer = True
        comp_admin.save()
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
    this form is created for creating users by super admin
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
                                  choices=(('admin', 'Super Admin'), ('suplier', 'Supplier Admin'), (
                                      'manufacturer', 'Manufacturer Admin'), ('customer', 'Customer'),)
                                  )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if self.cleaned_data.get("user_type") == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()
        if self.cleaned_data.get("user_type") == "suplier":
            user.is_company_admin = True
            user.is_staff = True
            user.save()
            comp_admin = CompanyAdmin.objects.create(user=user)
            comp_admin.is_suplier = True
            comp_admin.save()
        elif self.cleaned_data.get("user_type") == "manufacturer":
            user.is_company_admin = True
            user.is_staff = True
            user.save()
            comp_admin = CompanyAdmin.objects.create(user=user)
            comp_admin.is_manufacturer = True
            comp_admin.save()
        elif self.cleaned_data.get("user_type") == "customer":
            user.is_customer = True
            user.save()
            comp_admin = Customer.objects.create(user=user)
            comp_admin.save()
        return user


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
    user_group = forms.ModelChoiceField(
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
            self.cleaned_data.get("user_group")))
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
