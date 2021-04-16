from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum,Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from admin_site.models import CompanyDropdownsMaster
from admin_site.decorators import company_created,company_is_active

from company.models import Company
decorators = [never_cache, company_created(),company_is_active()]

# @method_decorator(decorators,name='dispatch')
def certification_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('certification__name').annotate(Count('id')).order_by('certification').exclude(main_category='FBPIDI')
    for certification in queryset:
        labels.append(certification['certification__name'])
        data.append(certification['id__count'])
    return JsonResponse({'labels':labels,'data':data})

def company_subsector_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('category__category_name').annotate(Count('id')).order_by('category').exclude(main_category='FBPIDI')
    for category in queryset:
        labels.append(category['category__category_name'])
        data.append(category['id__count'])
    return JsonResponse({'labels':labels,'data':data})


def management_tool_chart(request):
    labels=[]
    data=[]
    queryset = Company.objects.values('management_tools__name').annotate(Count('id')).order_by('management_tools').exclude(main_category='FBPIDI')
    for tools in queryset:
        labels.append(tools['management_tools__name'])
        data.append(tools['id__count'])
    return JsonResponse({'labels':labels,'data':data})  
    
def main_category_chart(request):
    labels = []
    data = []
    
    queryset = Company.objects.values('category__category_name').annotate(Count('id')).order_by('category').exclude(main_category='FBPIDI')
    for entry in queryset:
        labels.append(entry['category__category_name'])
        data.append(entry['id__count'])
    print(labels,data)
    print(queryset)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })