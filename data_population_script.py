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
from django.utils.timezone import localtime
from datetime import datetime

def set_token_for_existing_users():

    for user in User.objects.all():
        print("setting token for ", user.username)
        Token.objects.get_or_create(user=user)


def add_banks():
    names = ["Commerial Bank of Ethiopia ", "Addis International Bank", "Wogagen Bank", "Abyssiniya Bank"]
    for n in names:
        b = Bank(bank_name = n, bank_name_am =n, api_link=f"{n}'s api link")
        b.save()



if __name__ == '__main__':    
   
    m = ChatMessage.objects.first()
    t = m.timestamp
    print("t", t,"\n")
    p = datetime.strftime(t, "%y/%m/%d %H:%M:%S")
    print("\n first p", p, " ",type(p))
    pp= datetime.strptime(p, '%y/%m/%d %H:%M:%S')

    print("\n second p", pp, " ",type(pp))    
    now = datetime.now()
    
    if pp> now:
        print("greate")
    else:
        print("lesser")

