from django import template
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Company
from admin_site.models import Product


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