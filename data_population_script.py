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
    
    blogs = get_weekly_and_old(Blog.objects.filter(publish = True))
    if blogs['error']==False:
        this_week_objects = blogs['this_week_objects']
        older_blogs = blogs['older_objects']
        # current_site = get_current_site(request)
        blog_subject = ""
        if this_week_objects.count() > 0:
            mail_subject = f"Weekly notice of New Blogs and News with { this_week_objects.count() }"
            mail_message = "Check out this blogs, \n"
            for b in this_week_objects:
                mail_message+= f" {b.title} by {b.created_by.username} \n for more info click <a href='http://127.0.0.1:8000/collaborations/blog-detail/{b.id}/'> \n" 
        
        else:
            mail_subject = f"Blogs Notice from FBPIDI { older_blogs.count() }"
            mail_message = "Check out this blogs, \n"
            for b in older_blogs:
                mail_message+= f" {b.title} by {b.created_by.username} \n for more info click <a href='http://127.0.0.1:8000/collaborations/blog-detail/{b.id}/'> \n"         

        email = EmailMessage(mail_subject, mail_message,from_email="antenyismu@gmail.com", to=subscribers_email)
        email.content_subtype = "html"  
        try:
            email.send()
            print("Email sent ")
        except Exception as e:
            print("Exception While Sending Email ", str(e))
    else:
        print("Can't fetch blogs ", blogs)   
    
    # print(get_weekly_and_old(Blog.objects.filter(publish = True)))
    # print(get_weekly_and_old(News.objects.all()))
   
    # unnotified_blogs = Blog.objects.filter(publish = True, subscriber_notified = False)
    # week_dates  = [ timezone.now().date() - timedelta(days = d) for d in range(8)] #since we also need to subtract 7 days, the range has to b 8
    # week_blogs = unnotified_blogs.filter( created_date__date__in= week_dates )
    # week_blog_ids = [blog.id for blog in week_blogs]
    # older_blogs = unnotified_blogs.exclude(id__in = week_blog_ids)
    # print("week_blogs ", week_blogs)
    # print("older_blogs ", older_blogs)


    