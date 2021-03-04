from django import template
from django.core.exceptions import ObjectDoesNotExist
from company.models import Company,CompanyStaff
from product.models import Product
from chat.models import  ChatMessage, ChatGroup
from chat import views
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

register = template.Library()


@register.filter
def my_company_link(user):
    if user.is_superuser:
        try:
            co = Company.objects.get(company_type="fbpidi")
            return "/admin/view_fbpidi_company/"
        except ObjectDoesNotExist:
            return "/admin/create_fbpidi_company/"
    elif user.is_company_admin:
        try:
            co = Company.objects.get(user=user)
            return "/admin/view_company_profile/" 
        except ObjectDoesNotExist:
            return "/admin/create_company_profile/"
    elif user.is_company_staff:
        staff = CompanyStaff.objects.get(user=user)
        company = Company.objects.get(id=staff.company.id)
        return "/admin/view_company_profile/"

# count all unread messages
@register.simple_tag
def count_unread_messages(user):
    return ChatMessage.count_unread_message(user)


@register.simple_tag
def recieved_grouped_messages(user, max_num_group=None, exceluded = None):
        return views.get_recieved_grouped_messages(user, max_num_group, exceluded)


@register.simple_tag
def get_grouped_unread_messages(user): 
    return views.get_unread_grouped_messages(user)
@register.simple_tag
def get_all_messages_grouped(user, max_num_group=None, exceluded = None):
    return views.get_all_grouped_message(user, max_num_group, exceluded)
  