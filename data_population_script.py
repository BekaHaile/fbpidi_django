import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from accounts.models import User

from company.models import Bank, EventParticipants, CompanyEvent, Company
from accounts.models import User
from rest_framework.authtoken.models import Token
from company.api.serializers import *
from collaborations.models import *
from admin_site.api.serializers import *
from product.models import *
from product.api.serializer import *
from PIL import Image
from django.conf import settings
from chat.models import *
from django.db.models import Count

def set_token_for_existing_users():

    for user in User.objects.all():
        print("setting token for ", user.username)
        Token.objects.get_or_create(user=user)


def add_banks():
    names = ["Commerial Bank of Ethiopia ", "Addis International Bank", "Wogagen Bank", "Abyssiniya Bank"]
    for n in names:
        b = Bank(bank_name = n, bank_name_am =n, api_link=f"{n}'s api link")
        b.save()

def get_grouped_unread_messages(user):
    q = Q( Q(chat_group__group_name__contains = user.username) & Q( read = False) & ~Q(sender = user))
    unread_messages = ChatMessage.objects.filter(q).order_by('-timestamp') 
    print( get_grouped_message(unread_messages))


def get_grouped_recieved_messages(user):
    q = Q( Q(chat_group__group_name__contains = user.username)  & ~Q(sender = user))
    recieved_messages = ChatMessage.objects.filter(q).order_by('-timestamp')
    print(get_grouped_message(recieved_messages))
    


def get_grouped_message( list_of_messages):
    sender_names = []
    grouped = []
    for latest_sender_message in list_of_messages:
        if not latest_sender_message.sender.username in sender_names:
            print("new sender message", latest_sender_message.sender.username, " ", latest_sender_message.id)
            new = {
                'message':latest_sender_message,
                'count': list_of_messages.filter( sender__username = latest_sender_message.sender.username).count()
            }
            grouped.append(new)
            sender_names.append(latest_sender_message.sender.username)
    
    return grouped

            
# def append_sender_info(unread_messages, message):   
#         sender = message.sender
#         new = {}
#         new['sender'] = message.sender.username
#         if message.sender.profile_image:
#             new['image'] = message.sender.profile_image.url
#         else:
#             new['image'] = None 
#         new['count'] = unread_messages.filter(sender__username = message.sender.username).count()
#         new['timestamp'] = message.timestamp
#         return new

def get_grouped_messages(user, list_of_messages):
    pass


if __name__ == '__main__':    
    print(get_grouped_unread_messages(User.objects.get(username = 'third')))
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(get_grouped_recieved_messages(User.objects.get(username = 'third')))
    # print("Data population started ... ")
    # add_banks()
    # set_token_for_existing_users()
    # u = User.objects.get(username="third")
    # q = Q( Q(chat_group__group_name__contains = 'third') & Q( read = False) & ~Q(sender = u))
    
   
    # un = ChatMessage.objects.filter(q ) 
    # un = list(un)

    # m = ChatMessage.objects.filter(chat_group__group_name = 'postcustomer2_third', read = True)
    # grouped = {}
    # for c in un:
    #     sender = c.sender
    #     grouped[sender.username] = []
    #     for n in un:
    #         if n.sender.username == c.sender.username:
    #             grouped[sender.username].append(n)
        
               
    # print("##################3")
    # for j in un:
    #     print (j.id, ' ',j.sender,' ', j.content)

    # print("##################3")
    # for j in grouped['postcustomer2']:
     
    #      print (j.id, ' ',j.sender,' ', j.content)

    # print("$$$$$$$$ postcustomer2") 
    # for ke in grouped:
    #      print (ke)


    # for u in User.objects.all():
    #     u.email = "changedemailto_test_social_login@gmail.com"
    #     u.save()

    # print("done")
            
        
