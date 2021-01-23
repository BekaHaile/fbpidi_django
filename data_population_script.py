import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from fbpims.settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
import time
from company.models import Bank

print(type(AUTH_USER_MODEL))

def add_banks():
    names = ["Commerial Bank of Ethiopia ", "Addis International Bank", "Wogagen Bank", "Abyssiniya Bank"]
    for n in names:
        b = Bank(bank_name = n, bank_name_am =n, api_link=f"{n}'s api link")
        b.save()

if __name__ == '__main__':
    print("Data population started ... ")
    add_banks()
