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
      
    # print("Data population started ... ")
    # add_banks()
    # set_token_for_existing_users()
    
    b = NewsImages.objects.first()
    print(b.image.url)
    print(b.image.path)
    # image = Image.open(b.image)
    # cropped_image = image.crop((200.0,20.0,300.0, 100.0 ))
    # rs_image = cropped_image.resize((200,200), Image.ANTIALIAS)
    rs_image.save(b.image.path)
    print(b.image.url)
    
    
