import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from accounts.models import User

from company.models import Bank,  CompanyEvent, Company
from accounts.models import User
from rest_framework.authtoken.models import Token
from company.api.serializers import *
from company.models import *
from collaborations.models import *
from admin_site.api.serializers import *
from product.models import *
from product.api.serializer import *
from PIL import Image
from django.conf import settings
from chat.models import *
from django.db.models import Count
from django.utils.timezone import localtime
from datetime import datetime, timedelta


from django.db import connection, reset_queries
import time
import functools
from django.utils import timezone


def set_token_for_existing_users():

    for user in User.objects.all():
        print("setting token for ", user.username)
        Token.objects.get_or_create(user=user)


def add_banks():
    names = ["Commerial Bank of Ethiopia ", "Addis International Bank", "Wogagen Bank", "Abyssiniya Bank"]
    for n in names:
        b = Bank(bank_name = n, bank_name_am =n, api_link=f"{n}'s api link")
        b.save()

def filter_by_field_value_list():
    field_name = ['catagory', 'title'] # uses list of field name
    field_values = [ ['Beverage', 'Food'], ['Super user','From Post Man Edited'] ] # uses list of field value
    kwargs = {}
    q = Q()
    kwargs = {}
    n = News.objects.all()
    for i in range (len(field_name)):
        print("start filtering by ", field_name[i], " containing ", field_values[i])
        for value in field_values[i]:
            kwargs ['{0}__{1}'.format(field_name[i], 'contains')] = value
            q.add(Q(**kwargs),Q.OR)
            kwargs = {}

        
        n = n.filter(q)
        q = Q()
        print("result of filter by ", field_name[i],' containing ', field_values[i])
        for m in n:
            print(m.id," ", m.title," ", m.catagory)
        print('####################\n')


def filter_by(field_name, field_values, query_set):
    
    print("start filtering by ", field_name, " containing ", field_values," from ", query_set)
    kwargs ={}
    q= Q()
    for value in field_values:
        kwargs ['{0}__{1}'.format(field_name, 'contains')] = value
        q.add(Q(**kwargs),Q.OR)
        kwargs = {}
    query_set = query_set.filter(q)
    print("result of filter by ", field_name,' containing ', field_values)
    for m in query_set:
        print(m.id," ", m.title," ", m.catagory)
    print('####################\n')
    return query_set


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

models = { 'Announcement':Announcement, 'Blog':Blog, 'BlogComment':BlogComment, 'Choice':Choices, 'CompanyEvent':CompanyEvent, 'Tender':Tender, 'TenderApplicant':TenderApplicant, 
            'ForumQuestion':ForumQuestion, 'ForumComments':ForumComments, 'JobApplication':JobApplication, 'JobCategory':JobCategory, 'PollsQuestion':PollsQuestion, 'News':News }


def FilterByCompanyname(company_list,  query_set):
    try:
        q_object = Q()
        for company_name in company_list:
            q_object.add( Q(company__company_name = company_name ), Q.OR )
            q_object.add( Q(company__company_name_am = company_name ), Q.OR )
            
        query = query_set.filter(q_object)
        if query.count() == 0:
            query = query_set
            return { 'query': query, 'message': f"No match for found!" }
        return { 'query': query, 'message': f"{query.count()} result found!" }

    except Exception as e:
        print("Exception at FilterByCompanyName", str(e))


def search_title_related_objs( obj, query_list):
    return query_list.filter( Q(title__icontains = obj.title) | Q(title_am__icontains = obj.title_am) |Q(description__icontains = obj.title ) | Q(description_am__icontains = obj.title_am) ).distinct() 


@query_debugger
def filter_related_obj(model_name, obj):
    """
    given a modle name and an obj, searchs for other model objs with related company, if none found search for related objs with related title or description,
    if none found returns 4 elements from the model
    """
    model = models[model_name]
    return {'query': News.objects.select_related('company').all()}

    # result = FilterByCompanyname( [obj.get_company()], model.objects.exclude(id = obj.id))
    # if result['query'].count() == 0:
    #     result = search_title_related_objs(obj,result['query'] )
    #     if result.count() == 0:
    #         return {'query':model.objects.exclude(obj)[:4], 'message': f'Other {model_name}s ' }
    #     else:
    #         return {'query': result, 'message':f'Other {model_name}s with related content' }
    # else:
    #     return {'query':result['query'], 'message':f"Other {model_name}s from {obj.company.company_name} "}
    
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



if __name__ == '__main__':    
   u = User.objects.get(id = 1)
   c = ChatMessages.objects.filter( Q(sender = u)| )


    
    
    