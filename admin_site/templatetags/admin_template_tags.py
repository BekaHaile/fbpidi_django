from django import template
from django.core.exceptions import ObjectDoesNotExist
from company.models import Company,CompanyStaff
from product.models import Product
from chat.models import  ChatMessage, ChatGroup, get_recieved_grouped_messages, get_unread_grouped_messages
from django.db.models import Q

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
def unread_grouped_messages(user):
    return get_unread_grouped_messages(user)


@register.simple_tag
def recieved_grouped_messages(user):
    print("from admin template ",get_recieved_grouped_messages(user))
    return get_recieved_grouped_messages(user)


#### to be deleted
@register.simple_tag
def get_grouped_unread_messages(user):
    q = Q( Q(chat_group__group_name__contains = user.username) & Q( read = False) & ~Q(sender = user))
    un = ChatMessage.objects.filter(q).order_by('-timestamp')
    sender_names = []
    grouped = []
    for message in un:
        if not message.sender.username in sender_names:
            grouped.append(append_sender_info(un, message))
            sender_names.append(message.sender.username)
    
    return grouped

            
def append_sender_info(unread_messages, message):   
        sender = message.sender
        new = {}
        new['username'] = message.sender.username
        if message.sender.profile_image:
            new['image'] = message.sender.profile_image.url
        else:
            new['image'] = None 
        new['count'] = unread_messages.filter(sender__username = message.sender.username).count()
        new['chat_group'] = message.chat_group
        new['content'] = message.content
        new['timestamp'] = message.timestamp
        return new

    
    
        