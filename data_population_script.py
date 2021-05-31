
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from datetime import datetime
from django.utils import timezone
from product.models import *
from accounts.models import Customer, UserProfile
from collaborations.models import *


from company.models import *
# from admin_site.api.serializers import *
# from product.models import *
# from product.api.serializer import *
# from PIL import Image
from django.conf import settings
# from chat.models import *
from django.db.models import Count
from django.utils.timezone import localtime
from datetime import datetime, timedelta
# from company.api.serializers import *
# from collaborations.api.serializers import *

from django.db import connection, reset_queries
import time
import functools
from django.utils import timezone
# from background_task.models import Task

def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result
    return inner_func

@query_debugger
def with_select():
    for i in range(5):
        n = News.objects.all().select_related('company')
        print('with related\n')
        for m in n:
            print(m.title, " ", m.company.company_name),'\n'

@query_debugger
def with_out():
    for i in range(5):
        n = News.objects.all()
        print('with related\n')
        for m in n:
            print(m.title, " ", m.company.company_name),'\n'

def get_weekly_and_old(queryset):
    try:
        names = []
        u = UserProfile.objects.get(id = 1)
        print(u)
        
    except Exception as e:
        return {'error':True, 'message':str(e)}

if __name__ == '__main__':    
    c = Customer.objects.first()
    print(c)
    print(CompanyLike.objects.get(id = 34).user)
    print(CompanyLike.objects.filter(user= UserProfile.objects.get(id = 38)))


    
    