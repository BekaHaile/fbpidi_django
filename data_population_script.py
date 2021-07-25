
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()


from product.models import *
from accounts.models import  UserProfile
from collaborations.models import *
from accounts.email_messages import sendWeekBlogAndNews


from company.models import *
from django.db.models import Count, Aggregate, Avg, Max, Min, Sum
from django.utils.timezone import localtime
from datetime import datetime, timedelta

from django.db import connection, reset_queries
import time
import functools
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
        u = UserProfile.objects.get(id = 1)
        print(u)
        
    except Exception as e:
        return {'error':True, 'message':str(e)}


if __name__ == '__main__':    
    for c in Company.objects.all():
        c.color_theme = "#26236a"
        c.save()
        


    