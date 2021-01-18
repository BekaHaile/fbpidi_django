from django import template
from django.core.exceptions import ObjectDoesNotExist
<<<<<<< HEAD
from company.models import Company,CompanyStaff
from product.models import Product
=======
from accounts.models import Company,CompanyStaff
from admin_site.models import Product
>>>>>>> local/master


register = template.Library()


@register.filter
def my_company_link(user):
<<<<<<< HEAD
    if user.is_superuser:
        try:
            co = Company.objects.get(company_type="fbpidi")
            return "/admin/view_fbpidi_company/"
        except ObjectDoesNotExist:
            return "/admin/create_fbpidi_company/"
    elif user.is_company_admin:
=======
    if user.is_company_admin:
>>>>>>> local/master
        try:
            co = Company.objects.get(user=user)
            return "/admin/view_company_profile/" 
        except ObjectDoesNotExist:
            return "/admin/create_company_profile/"
    elif user.is_company_staff:
        staff = CompanyStaff.objects.get(user=user)
        company = Company.objects.get(id=staff.company.id)
        return "/admin/view_company_profile/"
        
