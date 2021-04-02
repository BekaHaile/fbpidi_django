from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum,Count

from admin_site.models import CompanyDropdownsMaster
from company.models import Company



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