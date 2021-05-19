import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from accounts.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string,get_template
# from accounts.api.serializers import CompanyAdminSerializer
# from rest_framework.authtoken.models import Token
# from company.api.serializers import *
# from company.models import *
from collaborations.models import *
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
from background_task.models import Task

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
        unnotified = queryset.filter(subscriber_notified = False)
        week_dates  = [ timezone.now().date() - timedelta(days = d) for d in range(8)] #since we also need to subtract 7 days, the range has to b 8
        this_week_objects = unnotified.filter( created_date__date__in= week_dates )
        week_obj_ids = [obj.id for obj in this_week_objects]
        older_objects = unnotified.exclude(id__in = week_obj_ids)
        return {'error':False, "this_week_objects": this_week_objects, "older_objects": older_objects}
    except Exception as e:
        return {'error':True, 'message':str(e)}

if __name__ == '__main__':    
    
    
    a = Announcement.objects.first()
    Announcement.objects.all().delete()
    print(Announcement.objects.all())


    