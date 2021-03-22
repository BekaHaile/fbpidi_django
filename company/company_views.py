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
    model = CompanyEvent
    template_name = "frontpages/company/company_vacancy_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['application_form'] = CreateJobApplicationForm
        return context


class CompanyBlogList(ListView):
    model = Blog
    template_name = "frontpages/company/company_blog.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return Blog.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
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

class CompanyPollDetail(DetailView):
    model = CompanyEvent
    template_name = "frontpages/company/company_event_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['company_pk'])
        context['event_participant_form'] = EventParticipantForm
        return context

