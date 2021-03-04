from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from company.models import Company
from product.models import Product
from admin_site.models import Category,SubCategory
from accounts.models import User
import datetime
from chat.models import ChatMessage, ChatGroup
import os
from chat import views as chat_views

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
def change_end_date(end_date):
            end_date =str(end_date)
            end_date = end_date[:19]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            return end_date 

image_formats = ['jpg',]

@register.simple_tag
def count_unread_messages(user):
    return ChatMessage.count_unread_message(user)


@register.simple_tag()
def file_type( file_url):
    name, file_extension = os.path.splitext(file_url) 
    if file_extension == '.jpg' or file_extension == '.png' or file_extension == '.gif' or file_extension == '.tiff':
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
def count_unread_messages(user):
    return ChatMessage.count_unread_message(user)


@register.simple_tag
def recieved_grouped_messages(user, max_num_group = None, exceluded = None):
        return chat_views.get_recieved_grouped_messages(user, max_num_group, exceluded)


@register.simple_tag
def get_grouped_unread_messages(user):  
    return chat_views.get_unread_grouped_messages(user)





