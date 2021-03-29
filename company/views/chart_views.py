from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum,Count

from admin_site.models import CompanyDropdownsMaster
from company.models import Company



def main_category_chart(request):
    labels = []
    data = []
    
    queryset = Company.objects.values('main_category').annotate(Count('id')).order_by('main_category').exclude(main_category='FBPIDI')
    for entry in queryset:
        labels.append(entry['main_category'])
        data.append(entry['id__count'])
    print(labels,data)
    print(queryset)
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })