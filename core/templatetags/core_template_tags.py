from django import template
from django.core.exceptions import ObjectDoesNotExist
from company.models import Company
from product.models import Product
from admin_site.models import Category,SubCategory

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
def company_count_bycategory(category):
    return Company.objects.filter(product_category=category).count()


@register.filter
def product_count_bycategory(category):
    return Product.objects.filter(category=category).count()