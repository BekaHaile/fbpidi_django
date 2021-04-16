
import json
import csv
import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.core import serializers
from django.db.models import Sum,Count,OuterRef,Exists,Q,F,Avg

from company.models import *
from product.models import *
from accounts.models import CompanyAdmin,UserProfile
from admin_site.decorators import company_created,company_is_active
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from company.forms import *
decorators = [never_cache, company_created(),company_is_active()]

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

@method_decorator(decorators,name='get')
class ProjectReport(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        projects = InvestmentProject.objects.all()
        # form of ownership
        queryset = projects.values('ownership_form').annotate(Count('id')).order_by('ownership_form') 
        total_ownership = 0
        ownership_data = []
        for ownership in queryset:
            total_ownership += int(ownership['id__count'])
            try:
                ownership_data.append({'label':CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']),
                                    'data':ownership['id__count']})
            except CompanyDropdownsMaster.DoesNotExist:
                ownership_data= []
        total_inv_cap_data = []
        for project in projects:
            if InvestmentCapital.objects.filter(project=project).exists():
                queryset =  InvestmentCapital.objects.filter(project=project).values('project__project_name').annotate(
                    machinery = Sum('machinery_cost'),
                    building = Sum('building_cost'),
                    working = Sum('working_capital')
                )
                for invcap in queryset:
                    total_inv_cap_data.append({
                        'project':invcap['project__project_name'],
                        'total_inv_cap':invcap['machinery']+invcap['working']+invcap['building'],
                        'machinery':invcap['machinery'],
                        'building':invcap['building'],
                        'working':invcap['working'],
                        'sector':project.sector
                    })
        queryset_classificaion = projects.values('project_classification').annotate(Count('id')).order_by('project_classification') 
        total_classification = 0
        classification_data = []
        for ownership in queryset_classificaion:
            total_classification += int(ownership['id__count'])
            try:
                classification_data.append({'label':ProjectDropDownsMaster.objects.get(id=ownership['project_classification']),
                                    'data':ownership['id__count']})
            except ProjectDropDownsMaster.DoesNotExist:
                classification_data= []
        prodn_data = []
        for project in projects:
            pdata = ProjectProductQuantity.objects.filter(project=project).values(
                'product_tobe_produced','expected_normal_capacity')
            for p in pdata:
                prodn_data.append({
                    'project':project.project_name,
                    'sector':project.sector,
                    'product':p['product_tobe_produced'],
                    'nominal_capacity':p['expected_normal_capacity']
                })
        emp_data_total = []
        total_perm_emp = 0
        total_temp_emp=0
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            
            for ep in employees_perm:
                total_perm_emp = (ep.male+ep.female)
            
            for et in employees_temp:
                total_temp_emp = (et.male+et.female)
            
            total = total_perm_emp+total_temp_emp
            emp_data_total.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        total_for_emp_m=0
        total_for_emp_f=0
        for_emp_data = []
        for project in projects:
            employees_foreign = Employees.objects.filter(projct=project,employment_type__icontains="Foreign")
            if employees_foreign.exists():
                for ef in employees_foreign:
                    total_for_emp_m += (ef.male)
                    total_for_emp_f += (ef.female)

                total = total_for_emp_m+total_for_emp_f
                for_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
        job_created_data = []
        for project in projects:
            jobs_created_temp = JobOpportunities.objects.filter(project=project,job_type__icontains="Temporary")
            jobs_created_permanent = JobOpportunities.objects.filter(project=project,job_type__icontains="Permanent")
            if jobs_created_temp.exists() or jobs_created_permanent.exists():
                temp_male = 0
                temp_female = 0
                for temp in jobs_created_temp:
                    temp_female += temp.female
                    temp_male += temp.male

                permanent_male = 0
                permanent_female = 0
                for p in jobs_created_permanent:
                    permanent_male += p.male
                    permanent_female += p.female

                job_created_data.append({'project':project.project_name,'sector':project.sector,'data':{
                    'temporary_male':temp_male,'temporary_female':temp_female,
                    'permanent_male':permanent_male,'permanent_female':permanent_female
                }})
        femal_emp_data = []
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            if employees_perm.exists() or employees_temp.exists():
                for ep in employees_perm:
                    total_perm_emp = (ep.female)
                
                for et in employees_temp:
                    total_temp_emp = (et.female)
                
                total = total_perm_emp+total_temp_emp
                femal_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        education_status_data = []
        total_edu = 0
        for project in projects:
            queryset_edu = EducationalStatus.objects.filter(
                project=project).values('education_type').annotate(
                     Sum('male'),Sum('female'),total_edu=Sum('male')+Sum('female') ).order_by('education_type')
            fem_edu = 0
            male_edu = 0
            if queryset_edu.exists():
                for edu_data in queryset_edu:
                    fem_edu += edu_data['female__sum']
                    male_edu += edu_data['male__sum']
                    # total_edu += int(+)
                    education_status_data.append({'project':project.project_name,'sector':project.sector,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})
            total_edu = fem_edu+male_edu
        context['filter_data'] = [
                                { 
                                    'data':projects.exclude(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects with export plan "
                                },
                                { 
                                    'data':projects.filter(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects wholly sell their product locally"
                                },
                                {
                                    'data':projects.exclude(Q(env_impac_ass_doc='')|Q(env_impac_ass_doc=None)),
                                    'label':"Number of investment projects that have Environmental impact assessment document"
                                },
                                ]
        
        context['total_edu'] = total_edu
        context['education_status_data'] = education_status_data
        context['total_fem_emp_data'] = femal_emp_data
        context['total_emp_data'] = emp_data_total
        context['job_created_data'] = job_created_data
        context['for_emp_data'] = for_emp_data
        context['nominal_data'] = prodn_data
        context['classification_data'] = classification_data
        context['total_class'] = total_classification
        context['inv_cap_data'] = total_inv_cap_data
        context['ownership_data'] = ownership_data
        context['total_ownership'] = total_ownership
        context['projects'] = projects
        context['regions']= RegionMaster.objects.all()
        return render(self.request,"admin/report/all_report_project.html",context)

    def post(self,*args,**kwargs):
        context = {}
        projects = InvestmentProject.objects.all()
        if self.request.POST['region'] != "":
            projects = projects.filter(project_address__region=self.request.POST['region'])
            
        if self.request.POST['sector'] != "":
            projects = projects.filter(sector=self.request.POST['sector'])

        if self.request.POST['sub_sector'] != "":
            projects = projects.filter(product_type=self.request.POST['sub_sector'])

        # form of ownership
        queryset = projects.values('ownership_form').annotate(Count('id')).order_by('ownership_form') 
        total_ownership = 0
        ownership_data = []
        for ownership in queryset:
            total_ownership += int(ownership['id__count'])
            try:
                ownership_data.append({'label':CompanyDropdownsMaster.objects.get(id=ownership['ownership_form']),
                                    'data':ownership['id__count']})
            except CompanyDropdownsMaster.DoesNotExist:
                ownership_data= []
        total_inv_cap_data = []
        for project in projects:
            if InvestmentCapital.objects.filter(project=project).exists():
                queryset =  InvestmentCapital.objects.filter(project=project).values('project__project_name').annotate(
                    machinery = Sum('machinery_cost'),
                    building = Sum('building_cost'),
                    working = Sum('working_capital')
                )
                for invcap in queryset:
                    total_inv_cap_data.append({
                        'project':invcap['project__project_name'],
                        'total_inv_cap':invcap['machinery']+invcap['working']+invcap['building'],
                        'machinery':invcap['machinery'],
                        'building':invcap['building'],
                        'working':invcap['working'],
                        'sector':project.sector
                    })
        queryset_classificaion = projects.values('project_classification').annotate(Count('id')).order_by('project_classification') 
        total_classification = 0
        classification_data = []
        for ownership in queryset_classificaion:
            total_classification += int(ownership['id__count'])
            try:
                classification_data.append({'label':ProjectDropDownsMaster.objects.get(id=ownership['project_classification']),
                                    'data':ownership['id__count']})
            except ProjectDropDownsMaster.DoesNotExist:
                classification_data= []
        prodn_data = []
        for project in projects:
            pdata = ProjectProductQuantity.objects.filter(project=project).values(
                'product_tobe_produced','expected_normal_capacity')
            for p in pdata:
                prodn_data.append({
                    'project':project.project_name,
                    'sector':project.sector,
                    'product':p['product_tobe_produced'],
                    'nominal_capacity':p['expected_normal_capacity']
                })
        emp_data_total = []
        total_perm_emp = 0
        total_temp_emp=0
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            
            for ep in employees_perm:
                total_perm_emp = (ep.male+ep.female)
            
            for et in employees_temp:
                total_temp_emp = (et.male+et.female)
            
            total = total_perm_emp+total_temp_emp
            emp_data_total.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        total_for_emp_m=0
        total_for_emp_f=0
        for_emp_data = []
        for project in projects:
            employees_foreign = Employees.objects.filter(projct=project,employment_type__icontains="Foreign")
            if employees_foreign.exists():
                for ef in employees_foreign:
                    total_for_emp_m += (ef.male)
                    total_for_emp_f += (ef.female)

                total = total_for_emp_m+total_for_emp_f
                for_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'for_male':total_for_emp_m,'for_female':total_for_emp_f})
        job_created_data = []
        for project in projects:
            jobs_created_temp = JobOpportunities.objects.filter(project=project,job_type__icontains="Temporary")
            jobs_created_permanent = JobOpportunities.objects.filter(project=project,job_type__icontains="Permanent")
            if jobs_created_temp.exists() or jobs_created_permanent.exists():
                temp_male = 0
                temp_female = 0
                for temp in jobs_created_temp:
                    temp_female += temp.female
                    temp_male += temp.male

                permanent_male = 0
                permanent_female = 0
                for p in jobs_created_permanent:
                    permanent_male += p.male
                    permanent_female += p.female

                job_created_data.append({'project':project.project_name,'sector':project.sector,'data':{
                    'temporary_male':temp_male,'temporary_female':temp_female,
                    'permanent_male':permanent_male,'permanent_female':permanent_female
                }})
        femal_emp_data = []
        total_fem_perm_emp = 0
        total_fem_temp_emp = 0
        for project in projects:
            employees_perm = Employees.objects.filter(projct=project,employment_type__icontains="Permanent")
            employees_temp = Employees.objects.filter(projct=project,employment_type__icontains="Temporary")
            if employees_perm.exists() or employees_temp.exists():
                for ep in employees_perm:
                    total_fem_perm_emp = (ep.female)
                
                for et in employees_temp:
                    total_fem_temp_emp = (et.female)
                
                total = total_fem_perm_emp+total_fem_temp_emp
                femal_emp_data.append({'project':project.project_name,'sector':project.sector,'data':total,'perm_emp':total_perm_emp,'temp_emp':total_temp_emp})
        education_status_data = []
        total_edu = 0
        for project in projects:
            queryset_edu = EducationalStatus.objects.filter(project=project).values('education_type').annotate(
                     Sum('male'),Sum('female'),total_edu=Sum('male')+Sum('female') ).order_by('education_type')
            fem_edu = 0
            male_edu = 0
            if queryset_edu.exists():
                for edu_data in queryset_edu:
                    fem_edu += edu_data['female__sum']
                    male_edu += edu_data['male__sum']
                    # total_edu += int(+)
                    education_status_data.append({'project':project.project_name,'sector':project.sector,'label':edu_data['education_type'],
                                        'data':int(edu_data['female__sum']+edu_data['male__sum'])})
            total_edu = fem_edu+male_edu
        context['filter_data'] = [
                                { 
                                    'data':projects.exclude(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects with export plan "
                                },
                                { 
                                    'data':projects.filter(Q(target_market='')|Q(target_market=None)), 
                                    'label':"Number of investment projects wholly sell their product locally"
                                },
                                {
                                    'data':projects.exclude(Q(env_impac_ass_doc='')|Q(env_impac_ass_doc=None)),
                                    'label':"Number of investment projects that have Environmental impact assessment document"
                                },
                                ]
        
        context['total_edu'] = total_edu
        context['education_status_data'] = education_status_data
        context['total_fem_emp_data'] = femal_emp_data
        context['total_emp_data'] = emp_data_total
        context['job_created_data'] = job_created_data
        context['for_emp_data'] = for_emp_data
        context['nominal_data'] = prodn_data
        context['classification_data'] = classification_data
        context['total_class'] = total_classification
        context['inv_cap_data'] = total_inv_cap_data
        context['ownership_data'] = ownership_data
        context['total_ownership'] = total_ownership
        context['projects'] = projects
        context['regions']= RegionMaster.objects.all()
        return render(self.request,"admin/report/all_report_project.html",context)