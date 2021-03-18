from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from company.models import Company,CompanyStaff
from product.models import Product
from chat.models import  ChatMessage, ChatGroup,ChatMessages
from chat import views
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone

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


@register.simple_tag
def user_create_button(user):
    if user.is_superuser:
        return mark_safe("/admin/create_user/")
    elif user.is_company_admin:
        try:
            Company.objects.get(user=user)
            return mark_safe("<a href='/admin/create-my-staff/' class='btn bg-teal btn-sm rounded-round'><i class='icon-add mr-2'></i>Create Staff</a>")
        except ObjectDoesNotExist:
            return mark_safe("<a href='/admin/create_company_profile/' class='btn bg-red btn-sm rounded-round'><i class='icon-add mr-2'></i>Please Create Your Company Profile</a>")

# count all unread messages
@register.simple_tag
def count_unread_messages(user):
    return ChatMessages.count_unread_messages(user)



@register.simple_tag
def get_date(date):
    return date.date()
