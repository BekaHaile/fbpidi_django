import datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone


from company.models import *
from product.models import *
from accounts.models import UserProfile

register = template.Library()


def get_current_year():
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day

    if month <= 7 and day < 8 or month <= 7:
        current_year = gc_year-9
    else:
        current_year = gc_year - 8
    return current_year

def in_between(x,min,max):
    return ((x-min)*(x-max) <= 0)

def get_current_year_half():
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if in_between(month,1,6):
        current_year = gc_year-8
    else:
        current_year = gc_year - 9
    return current_year

def get_current_year_quarter():
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if in_between(month,10,12) or in_between(month,1,3) or in_between(month,4,6):
        current_year = gc_year-8
    else:
        current_year = gc_year - 9
    return current_year
def get_current_half():
    month = datetime.datetime.today().month
    half = ""
    if in_between(month,1,6):
        quarter = "First_Half"
    elif in_between(month, 7, 12):
        quarter = "Second_Half"
    return half

def get_current_quarter():
    month = datetime.datetime.today().month
    quarter = ""
    if in_between(month,4,6):
        quarter = "Fourth_Quarter"
    elif in_between(month, 1, 3):
        quarter = "Third_Quarter"
    elif in_between(month, 7, 9):
        quarter = "First_Quarter"
    elif in_between(month, 10, 12):
        quarter = "Second_Quarter"
    return quarter


@register.filter
def alert_employees_data(company):
    try:
        company = Company.objects.get(id=company)
        employee_data = Employees.objects.filter(company=company,year_emp=get_current_year())
        if employees_data.exists():
            return True
        else:
            return False
    except Exception as e:
        return True

@register.filter
def alert_production_capacity_data(company):
    try:
        company = Company.objects.get(id=company)
        pcap_data = ProductionCapacity.objects.filter(company=company,year=get_current_year())
        if pcap_data.exists():
            return True
        else:
            return False
    except Exception as e:
        return True

@register.filter
def alert_input_need_data(company):
    try:
        company = Company.objects.get(id=company)
        input_need_data = AnnualInputNeed.objects.filter(company=company,year=get_current_year())
        if input_need_data.exists():
            return True
        else:
            return False
    except Exception as e:
        return True

@register.filter
def alert_demand_suply_data(company):
    try:
        company = Company.objects.get(id=company)
        demand_supply = InputDemandSupply.objects.filter(company=company,year=get_current_year())
        if demand_supply.exists():
            return True
        else:
            return False
    except Exception as e:
        return True


@register.filter
def alert_sales_performance_data(company):
    half = ""
    if get_current_half() == "First_Half":
        half = ""
    elif get_current_half() == "Second_Half":
        half = "First_Half"

    flag = False
    try:
        company = Company.objects.get(id=company)
        if quarter != "":
            sales_performance = ProductionAndSalesPerformance.objects.filter(
                company=company,
                activity_year=get_current_year_half(),half_year=half
            )

            if sales_performance.exists():
                flag =  True
            else:
                flag =  False
        else:
            flag =  True
    except Exception as e:
        flag =  True
    return flag


@register.filter
def alert_job_created_data(company):
    quarter = ""
    if get_current_quarter() == "Fourth_Quarter":
        quarter = "Third_Quarter"
    elif get_current_quarter() == "Third_Quarter":
        quarter = "Second_Quarter"
    elif get_current_quarter() == "Second_Quarter":
        quarter = "First_Quarter"
    elif get_current_quarter() == "First_Quarter":
        quarter = ""
    flag = False
    try:
        company = Company.objects.get(id=company)
        if quarter != "":
            jobs_created = JobOpportunities.objects.filter(
                company=company,
                year_job=get_current_year_quarter(),quarter_job=quarter
            )

            if jobs_created.exists():
                flag =  True
            else:
                flag =  False
        else:
            flag =  True
    except Exception as e:
        flag =  True
    return flag


@register.filter
def alert_edu_status_data(company):
    quarter = ""
    if get_current_quarter() == "Fourth_Quarter":
        quarter = "Third_Quarter"
    elif get_current_quarter() == "Third_Quarter":
        quarter = "Second_Quarter"
    elif get_current_quarter() == "Second_Quarter":
        quarter = "First_Quarter"
    elif get_current_quarter() == "First_Quarter":
        quarter = ""
    flag = False
    try:
        company = Company.objects.get(id=company)
        if quarter != "":
            edu_status = EducationalStatus.objects.filter(
                company=company,
                year_edu=get_current_year_quarter(),quarter_edu=quarter
            )

            if edu_status.exists():
                flag =  True
            else:
                flag =  False
        else:
            flag =  True
    except Exception as e:
        flag =  True
    return flag


@register.filter
def alert_female_emp_data(company):
    quarter = ""
    if get_current_quarter() == "Fourth_Quarter":
        quarter = "Third_Quarter"
    elif get_current_quarter() == "Third_Quarter":
        quarter = "Second_Quarter"
    elif get_current_quarter() == "Second_Quarter":
        quarter = "First_Quarter"
    elif get_current_quarter() == "First_Quarter":
        quarter = ""
    flag = False
    try:
        company = Company.objects.get(id=company)
        if quarter != "":
            female_emps = FemalesInPosition.objects.filter(
                company=company,
                year_fem=get_current_year_quarter(),quarter_fem=quarter
            )

            if female_emps.exists():
                flag =  True
            else:
                flag =  False
        else:
            flag =  True
    except Exception as e:
        flag =  True
    return flag