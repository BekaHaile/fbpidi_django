from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from company.models import Company
from product.models import Product
from admin_site.models import Category,SubCategory
from accounts.models import User
import datetime
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


@register.filter
def change_start_date(start_date):
        start_date =str(start_date)
        start_date =start_date[:19]
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        return start_date

@register.simple_tag
def change_end_date(end_date):
            end_date =str(end_date)
            end_date = end_date[:19]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            return end_date 

@register.simple_tag
def get_company_name(tender):
    if tender:
        return tender.get_company().company_name 
    else:
        return "NO Company!"

@register.simple_tag
def mukera(user):
    return user.username

