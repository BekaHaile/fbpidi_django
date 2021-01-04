from django import template
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Company,CompanyStaff
from admin_site.models import Product


register = template.Library()


@register.filter
def my_company_link(user):
    if user.is_company_admin:
        try:
            co = Company.objects.get(user=user)
            return "/admin/comp_profile/view/1/" 
        except ObjectDoesNotExist:
            return "/admin/comp_profile/create/1/"
    elif user.is_company_staff:
        staff = CompanyStaff.objects.get(user=user)
        company = Company.objects.get(id=staff.company.id)
        return "/admin/comp_profile/view/1/"
        
