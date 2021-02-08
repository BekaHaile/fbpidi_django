import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from fbpims.settings import AUTH_USER_MODEL
from accounts.models import User
import time
import datetime

from company.models import Bank, EventParticipants, CompanyEvent

def add_banks():
    names = ["Commerial Bank of Ethiopia ", "Addis International Bank", "Wogagen Bank", "Abyssiniya Bank"]
    for n in names:
        b = Bank(bank_name = n, bank_name_am =n, api_link=f"{n}'s api link")
        b.save()

def mukera():
    c = CompanyEvent.objects.first()
    now = datetime.datetime.now()
    print("date time ", datetime.timedelta, " type ", type(datetime.datetime.day))
    print("start date", c.start_date, "type ", type(c.start_date))
    print(type(now), " ",datetime.datetime.now()," ", c.start_date)
    cc = str(c.start_date.date)
    if  now.day > c.start_date.day:
        print("greater than by ", now.day - c.start_date.day)
    else:
        print("lesser than by ", c.start_date - now)
    
def change_notify():
    c =EventParticipants.objects.all()

    for n in c:
        n.notifiy_in = 1
        n.notified = False
        n.save()
        print("Finished")
    print(c)

if __name__ == '__main__':
    print("Data population started ... ")
    # add_banks()
    # change_notify()

    b=User.objects.get(id=3)
    print(b.user_permissions.all().count())
    for i in b.user_permissions.all():
        if "add_faq" == i.codename:
            print("-----");