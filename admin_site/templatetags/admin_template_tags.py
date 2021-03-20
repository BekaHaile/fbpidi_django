from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone


from company.models import Company,CompanyStaff
from product.models import Product
from chat.models import  ChatMessage, ChatGroup,ChatMessages
from chat import views


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
        return int(Company.objects.all().count())


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
def count_unread_messages(user):
    return ChatMessages.count_unread_messages(user)

@register.simple_tag
def tag_edit(string):
    tag_list = string.split(',')
    return tag_list

 
@register.simple_tag
def printstr(string):
    print(string) 


@register.simple_tag
def get_date(date):
    return date.date()
