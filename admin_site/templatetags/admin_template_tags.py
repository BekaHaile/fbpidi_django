from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone


from company.models import Company,CompanyStaff, CompanyMessage
from product.models import Product, ProductInquiry
from chat.models import  ChatMessages, Notification
from chat import views
from collaborations.models import Document, Document_Category


from accounts.models import UserProfile

register = template.Library()

@register.filter
def get_company_id(user):
    user = UserProfile.objects.get(id=user.id)
    if user.get_company() != None:
        return user.get_company().id
        print(user.get_company().id)
    else:
        return 0

@register.filter
def company_count(user):
    if user.is_authenticated:
        return int(Company.objects.all().exclude(main_category="FBPIDI").count())

@register.simple_tag
def add_two_val(x,y):
    return float(x+y)
    
@register.filter
def get_sum(data):
    sm = 0
    for d in data:
        sm+=d['data']
    return sm

@register.filter
def get_total_prodn(data):
    total = 0
    for tpa in data:
        total += tpa['production_amount']
    return total

@register.filter
def get_total_actual(data):
    total = 0
    for tpa in data:
        total += tpa['actual_production']
    return total

@register.simple_tag
def get_capital_util(x,y):
    if float(y) > 0:
        return round(float(float(x)/(float(y)*260))*100,2)
    elif float(y) == 0:
        return round(float(float(x)/(1))*100,2)

@register.simple_tag
def get_inv_cap_sum(data,option):
    print(option)
    total = 0
    if option == 'machinery':
        for i in data:
            total += i['machinery']
    
    if option == 'building':
        for i in data:
            total += i['building']
    if option == 'working':
        for i in data:
            total += i['working']
    
    if option == 'total':
        for i in data:
            total += i['total_inv_cap']

    return round(total,2)

@register.simple_tag
def get_prodn_total(data,option):
    total = 0
    if option == 'prodn':
        for d in data:
            total += d['total_data']['installed']
    
    if option == 'actual':
        for d in data:
            total += d['total_data']['actual']

    return round(total,2)

@register.simple_tag
def change_capital_util(thisd,last,pdata):
    if pdata == 0:
        return round((float(thisd)-float(last))/1,2) 
    else:
        return round((float(thisd)-float(last))/(12 * float(pdata)),2)

@register.simple_tag
def change_util_total(data,option):
    total = 0
    if option == 'thisyear':
        for d in data:
            total += d['pa_this']

    if option == 'lastyear':
        for d in data:
            total += d['pa_last']
    
    if option == 'apc':
        for d in data:
            total += d['apc']
    
    if option == 'total':
        x=0
        y=0
        a =0
        for d in data:
            x += d['pa_this']
            y += d['pa_last']
            a += d['apc']
        if a == 0:
            total = (x-y)
        else:
            total = (x-y)/a

    return round(total,2)

@register.simple_tag
def get_percent(x,y):
    return round(float(x/y)*100,2)



@register.simple_tag
def get_share(data,total):
    print(type(data),type(total))
    if total > 0:
        return round(float(int(data)/int(total))*100,2)
    else:
        return round(float(int(data)/int(1))*100,2)

@register.simple_tag
def user_create_button(user):
    if user.is_superuser:
        return mark_safe("/admin/create_user/")
    elif user.is_company_admin:
        try:
            Company.objects.get(contact_person=user)
            return mark_safe("<a href='/admin/create-my-staff/' class='btn bg-teal btn-sm rounded-round'><i class='icon-add mr-2'></i>Create Staff</a>")
        except ObjectDoesNotExist:
            return mark_safe("<a href='/admin/create_company_profile/' class='btn bg-red btn-sm rounded-round'><i class='icon-add mr-2'></i>Please Create Your Company Profile</a>")

# count all unread messages
@register.simple_tag
def count_unread_chats(user):
    return ChatMessages.count_unread_chats(user)

@register.simple_tag
def count_unread_inbox(company):
    return CompanyMessage.objects.filter(company = company, replied =False).count()

@register.simple_tag
def count_notifications(user):
    return Notification.new_notifications(user).count()

@register.simple_tag
def count_new_inquiry_requests(user_company):
    return ProductInquiry.objects.filter(product__company = user_company, replied=False).count()

@register.simple_tag
def count_pending_products(company=None):
    if company!=None:
        return Product.objects.filter(company = company.id, is_active=False).count()
    return Product.objects.filter(is_active = False).count()
    

@register.simple_tag
def tag_edit(string):
    tag_list = string.split(',')
    return tag_list

 
@register.simple_tag
def printstr(string):
    print(string) 

@register.simple_tag
def count_documents(category, user):
  return  (Document.objects.filter( category = category, company = user.get_company()) ).count()

@register.simple_tag
def get_date(date):
    return date.date()
