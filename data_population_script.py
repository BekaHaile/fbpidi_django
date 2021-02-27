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
    file_name = "one.two.three.four"
    doc = Document.objects.first()
    name, extension = os.path.splitext(doc.document.url)
    print("name = ", name, " ext = ", extension)

    # print(file_name)
    # for i in file_name[-1:]:

    #     print(i,"\n")
    #     # if i == '.':
    #     index  = file_name.index(i,) 
    #     print("index = ", index, file_name[index:-1])
    # print("Data population started ... ")
    # add_banks()
    # set_token_for_existing_users()
    
            
    
