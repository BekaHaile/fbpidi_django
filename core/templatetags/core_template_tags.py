from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from company.models import Company
from product.models import Product
from admin_site.models import Category,SubCategory
from accounts.models import User
register = template.Library()


@register.filter
def company_count(type):
    try:
        co = Company.objects.filter(company_type=type)
        return co.count() 
    except ObjectDoesNotExist:
        return 0


@register.filter
def company_product_count(company):
    try:
        product = Product.objects.filter(user=company.user)
        return product.count()
    except ObjectDoesNotExist:
        return 0

@register.filter
def product_count(non):
    product = Product.objects.all()
    return product.count()

@register.filter
def happy_customer(non):
    return User.objects.all().count()


@register.filter
def company_count_bycategory(category):
    return Company.objects.filter(product_category=category).count()


@register.filter
def product_count_bycategory(category):
    return Product.objects.filter(category=category).count()

@register.simple_tag
def print_translated(en_data,am_data,lan_code):
    if lan_code == "en":
        return mark_safe(en_data)
    elif lan_code == 'am':
        return mark_safe(am_data)

@register.simple_tag
def get_company_name(tender):
    if tender:
        return tender.get_company().company_name 
    else:
        return "NO Company!"

@register.filter
def get_user_company(user):
    if user.is_company_admin:
        return Company.objects.get(user = user)
    elif user.is_company_staff:
        return Company.objects.get(user = user)


@register.filter
def get_user_company_name(user):
    if user.is_company_admin:
        return Company.objects.get(user = user).company_name
    elif user.is_company_staff:
        return Company.objects.get(user = user).company_name

