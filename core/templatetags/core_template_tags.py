from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from company.models import Company
from product.models import SubCategory,Product,Review
from admin_site.models import Category
from accounts.models import UserProfile
import datetime
from chat.models import ChatMessages
import os
from chat import views as chat_views

register = template.Library()

@register.filter
def review_count(product):
    return Review.objects.filter(product=product).count()

@register.filter
def company_count(type):
    try:
        return Company.objects.all().exclude(main_category="FBPIDI").count()
    except ObjectDoesNotExist:
        return 0


@register.filter
def company_product_count(company):
    try:
        product = Product.objects.filter(company=company)
        return product.count()
    except ObjectDoesNotExist:
        return 0


@register.filter
def product_count(non):
    product = Product.objects.all()
    return product.count()


@register.filter
def happy_customer(non):
    return UserProfile.objects.all().count()


@register.simple_tag
def printstr(string):
    print(string) 


@register.filter
def company_count_bycategory(category):
    return Company.objects.filter(category=category).count()


@register.filter
def product_count_bycategory(category):
    category = Category.objects.get(id=category)
    brands = []
    sub_categories = category.sub_category.all()
    for sub_cat in sub_categories:
        for brand in sub_cat.product_category.all():
            brands.append(brand)
    return Product.objects.filter(brand__in=brands).count()
    # if category.category_type == "Pharmaceuticals":
    #     return Product.objects.filter(pharmacy_category=category).count()
    # elif category.category_type == "Food" or category.category_type == "Beverage":
        
@register.filter
def product_count_by_subcategory(sub_category):
    try:
        sub_category = SubCategory.objects.get(id=sub_category)
        product = Product.objects.filter(brand__product_type=sub_category).count()
        return product
    except Exception as e:
        return 0
        
@register.filter
def count_food_and_beverage_products(category):
    category = Category.objects.get(id=category)
    brands = []
    sub_categories = category.sub_category.all()
    for sub_cat in sub_categories:
        for brand in sub_cat.product_category.all():
            brands.append(brand)
    return Product.objects.filter(fandb_category__in=brands).count()

@register.filter
def pharmacy_product_count(category):
    return Product.objects.filter(pharmacy_category=category).count()


@register.simple_tag
def print_translated(en_data,am_data,lan_code):
    if lan_code == "en":
        return mark_safe(en_data)
    elif lan_code == 'am':
        return mark_safe(am_data)


@register.simple_tag
def change_end_date(end_date):
        end_date =str(end_date)
        end_date = end_date[:19]
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
        return end_date 


@register.simple_tag()
def file_type( file_url):
    name, file_extension = os.path.splitext(file_url) 
    if file_extension == '.jpg' or file_extension == '.jpeg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff':
        return "image"
    elif  file_extension == '.mp4' or file_extension == '.avi' or file_extension == '.mov' or file_extension == '.wmv':
        return "video"
    elif  file_extension == '.mp3' or file_extension == '.wav' or file_extension == '.aac' or file_extension == '.wma' or file_extension == '3gpp':
        return "audio"
    elif file_extension == '.pdf':
        return "pdf"
    elif file_extension == '.docx' or file_extension == '.doc' :
        return "word"
    elif file_extension == '.xlsx':
        return "excel"
    elif file_extension == '.exe':
        return "exe"
    else:
        return ""

# count all unread messages
@register.simple_tag
def count_unread_chats(user):
    return ChatMessages.count_unread_chats(user)

@register.simple_tag
def user_liked_product(user, product):    
    return True if user.productlike_set.filter(product = product).exists()  else  False

@register.simple_tag
def user_liked_company(user, company):    
    return True if user.companylike_set.filter(company = company).exists()  else  False

@register.simple_tag
def get_fbpidi():
    return Company.objects.get(main_category="FBPIDI") if Company.objects.filter(main_category = "FBPIDI") else None


@register.simple_tag
def count_review_rating(product, rating):
    return product.review_set.filter(rating = rating).count()

    






