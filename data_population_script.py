import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from fbpims.settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
import time
import datetime

from company.models import Bank, EventParticipants, CompanyEvent
from accounts.models import User
from rest_framework.authtoken.models import Token


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
    set_token_for_existing_users()
    