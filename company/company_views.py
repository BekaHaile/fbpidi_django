import datetime
import json
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.utils import timezone
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.core import serializers

from company.models import *
from accounts.models import CompanyAdmin,User
from product.models import Order,OrderProduct,Product

from company.forms import *
from collaborations.models import *
from collaborations.forms import EventParticipantForm,TenderApplicantForm,CreateJobApplicationForm
from chat.models import ChatMessages
class CompanyHomePage(DetailView):
    model = Company
    template_name="frontpages/company/business-5.html"  

class CompanyAbout(DetailView):
    model=Company
    template_name="frontpages/company/about.html"


class CompanyContact(DetailView):
    model=Company
    template_name="frontpages/company/contact.html"

class CompanyProductList(DetailView):
    model= Company
    template_name = "frontpages/company/blog-grid-center.html"

class CompanyProjectList(DetailView):
    model= Company
    template_name = "frontpages/company/blog-grid-center.html"

class CompanyNewsList(ListView):
    model = News
    template_name = "frontpages/company/company_news.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return News.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "#######3 the excptio is ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyNewsDetail(DetailView):
    model = News
    template_name = "frontpages/company/company_news_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        return context


class CompanyEventList(ListView):
    model = CompanyEvent
    template_name = "frontpages/company/company_events.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return CompanyEvent.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### while listing company events ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyEventDetail(DetailView):
    model = CompanyEvent
    template_name = "frontpages/company/company_event_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['event_participant_form'] = EventParticipantForm
        return context


class CompanyAnnouncementList(ListView):
    model = Announcement
    template_name = "frontpages/company/company_announcement.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Announcement.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company Announcement ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context
        

class CompanyAnnouncementDetail(DetailView):
    model = Announcement
    template_name = "frontpages/company/company_announcement_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        return context


class CompanyResearchList(ListView):
    model = Research
    template_name = "frontpages/company/company_research.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Research.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company events ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyTenderList(ListView):
    model = Tender
    template_name = "frontpages/company/company_tenders.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Tender.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company tender ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context

class CompanyTenderDetail(DetailView):
    model = Tender
    template_name = "frontpages/company/company_tender_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['applicant_form'] = TenderApplicantForm
        return context



class CompanyVacancyList(ListView):
    model = Vacancy
    template_name = "frontpages/company/company_vacancy.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Vacancy.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company events ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        context['application_form'] = CreateJobApplicationForm
        return context


class CompanyVacancyDetail(DetailView):
    model = Vacancy
    template_name = "frontpages/company/company_vacancy_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['application_form'] = CreateJobApplicationForm
        return context





class CompanyVacancyApply(LoginRequiredMixin,CreateView):
    model = JobApplication
    template_name = "frontpages/company/company_vacancy_apply.html"
    form_class = CreateJobApplicationForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        vacancy =  Vacancy.objects.get(id=self.kwargs['vacancy_pk'] )
        context['obj'] = vacancy
        context['object'] = vacancy.company
        context['category'] = JobCategory.objects.all()
        return context

    def form_valid(self,form):
        job=form.save(commit=False)
        job.user=self.request.user
        job.vacancy = Vacancy.objects.get(id=self.kwargs['vacancy_pk'])
        job.save()
        print("############### object saved on ", job.id)
        return redirect(f"/company/company_vacancy_detail/{job.vacancy.id}")
    def form_invalid(self,form):
        messages.warning(self.request, "Unsupported file type detected, the supported files are pdf, jpg, png, doc and docx! ")
        vacancy=Vacancy.objects.get(id = self.kwargs['vacancy_pk'])
        return redirect(f"/company/company_vacancy_apply/{vacancy.id}/")


class CompanyBlogList(ListView):
    model = Blog
    template_name = "frontpages/company/company_blog.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Blog.objects.filter(company = Company.objects.filter(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company events ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyBlogDetail(DetailView):
    model = CompanyEvent
    template_name = "frontpages/company/company_event_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['event_participant_form'] = EventParticipantForm
        return context


class CompanyPollList(ListView):
    model = PollsQuestion
    template_name = "frontpages/company/company_poll.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return PollsQuestion.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company events ",e)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyPollDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        message = ""
        context = {}        
        try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                context ['obj'] = poll
                context ['object'] = poll.company
                if poll.pollsresult_set.filter(user = self.request.user).count() > 0:
                    context ['has_voted'] = True
                return render(self.request, "frontpages/company/company_poll_detail.html", context)
        except Exception as e:
                print( "Poll not found ",e)
                return redirect("polls") 
        
    def post(self,*args,**kwargs):
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
                vote = PollsResult(poll = poll,user = self.request.user,choice = Choices.objects.get(id = self.request.POST['selected_choice']),
                    remark=self.request.POST['remark'] )
                vote.save()
                print( "Successfully voted!")
                return redirect(f"/company/company_poll/{poll.company.id}/") 
            except Exception as e:
                messages.warning(self.request, "Poll not found!",e)
                return redirect("polls") 
        


