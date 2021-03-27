import datetime
import json
from django.urls import reverse
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
from accounts.email_messages import sendRelayMessage
from product.models import Order,OrderProduct,Product

from company.forms import *
from collaborations.models import *
from chat.models import ChatMessages
from collaborations.forms import EventParticipantForm,TenderApplicantForm,CreateJobApplicationForm, BlogCommentForm



class CompanyHomePage(DetailView):
    model = Company
    template_name="frontpages/company/company_index.html"  


class CompanyAbout(DetailView):
    model=Company
    template_name="frontpages/company/about.html"


# class CompanyContact(DetailView):
#     model=Company
#     template_name="frontpages/company/contact.html"



class CompanyContact(CreateView):
    model = CompanyMessage
    template_name = "frontpages/company/contact.html"
    form_class = CompanyMessageForm
    
    def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(**kwargs)
            context['object']  = Company.objects.get(id = self.kwargs['pk'])
            return context
        
    def form_valid(self, form):
        try:
            comp_message = form.save(commit = False)
            comp_message.company = Company.objects.get (id = self.kwargs['pk'])
            comp_message.save()
            if comp_message.company.main_category == "FBPIDI": # if the contacted company is FBPIDI
                return redirect('index')
            return redirect(f"/company/company-home-page/{self.kwargs['pk']}/") 
        except Exception as e:
            print("@@@@@@@@ Exception at company Contact Form ", e)
            return redirect(f"/company/contact/{self.kwargs['pk']}/")   

    def form_invalid(self, form):
        messages.warning(self.request, "Wrong Form Input!")
        return redirect(f"/company/contact/{self.kwargs['pk']}/")


class CompanyInboxList(ListView):
    model = CompanyMessage
    template_name = "admin/company/inbox_list.html"
    context_object_name = "message_list"
    def get_queryset(self):
        print(self.request.GET)
        if 'replied_only' in self.request.GET:
            print("inside replied_only")
            return CompanyMessage.objects.filter(company = self.request.user.get_company().id, replied =True)
        elif 'unreplied_only' in self.request.GET:
            print("inside unreplied_only")
            return CompanyMessage.objects.filter(company = self.request.user.get_company().id, replied = False)
        print("inside All")
        return CompanyMessage.objects.filter(company = self.request.user.get_company().id)


class CompanyInboxDetail(View):
    # def get(self, *args, **kwargs):
    #     message = CompanyMessage.objects.get(id = self.kwargs['pk'])
    #     message.seen = True
    #     message.save()
    #     return render(self.request, 'admin/company/admin_inbox_detail.html',{'message':message} )

    def post(self, *args, **kwargs):
        try:
            sender_message = CompanyMessage.objects.get(id = self.kwargs['pk'])
            reply_message = self.request.POST['reply_message']
            if sendRelayMessage(self.request, sender_message, reply_message): #returns true if the email is sent successfully
                sender_message.replied = True
                sender_message.save()
                reply= CompanyMessageReply(created_by=self.request.user, message=sender_message, reply_message =reply_message)
                reply.save()
                messages.success(self.request, f"Successfully, replied to {message.email}")
                return redirect('admin:admin_inbox_list')
            else:
                messages.warning(self.request, f"Reply couldn't be sent! Please check your connection and try again later.")
                return redirect('admin:admin_inbox_list')
        except Exception as e:
            print("########## Exception at CompanyInboxDetail post ",e)
            messages.warning(self.request, "########## Exception at CompanyInboxDetail post ",e)
            return redirect("admin:index")

        



class CompanyProductList(DetailView):
    model= Company
    template_name = "frontpages/company/product_list.html"

class CompanyProductdetail(DetailView):
    model=Product
    template_name = "frontpages/company/product_details.html"
    context_object_name = "product"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Product.objects.get(id=self.kwargs['pk']).company
        return context

class CompanyProjectList(DetailView):
    model= Company
    template_name = "frontpages/company/project_list.html"

class CompanyProjectdetail(DetailView):
    model=InvestmentProject
    template_name = "frontpages/company/project_detail.html"
    context_object_name = "project"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = InvestmentProject.objects.get(id=self.kwargs['pk']).company
        return context


class CompanyNewsList(ListView):
    model = News
    template_name = "frontpages/company/company_news.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return News.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "#######3 the excption is ",e)
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
            return []
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
            return []
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Company.objects.get(id =self.kwargs['pk'])
        return context


class CompanyResearchDetail(DetailView):
    model = Research
    template_name = "frontpages/company/company_research_detail.html"
    context_object_name = "obj"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['object'] = Research.objects.get(id = self.kwargs['pk'] ).company
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
            return []
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
            return []
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
        return redirect(f"/company/company_vacancy_detail/{job.vacancy.id}")
    def form_invalid(self,form):
        messages.warning(self.request, "Unsupported file type detected, the supported files are pdf, jpg, png, doc and docx! ")
        vacancy=Vacancy.objects.get(id = self.kwargs['vacancy_pk'])
        return redirect(f"/company/company_vacancy_apply/{vacancy.id}/")


# class CompanyBlogList(ListView):
#     model = Blog
#     template_name = "frontpages/company/company_blog.html"
#     paginate_by = 2
#     def get_queryset(self):
#         try:
#             return Blog.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
#         except Exception as e:
#             print( "####### Exception while gettng company blog ",e)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs) 
#         context['object'] = Company.objects.get(id =self.kwargs['pk'])
        
#         return context


class CompanyBlogList(ListView):
        model = Blog
        template_name="frontpages/company/company_blog.html"
        paginate_by = 2
        def get_queryset(self):
            return Blog.objects.filter( company = Company.objects.get(id = self.kwargs['pk']) , publish=True)

        def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(**kwargs)
            context['object'] = Company.objects.get(id = self.kwargs['pk'])
            return context

        
def get_tags(lang, company):
        comp_blogs = Blog.objects.filter(company = company, publish=True)
        string = ""
        if(lang =="amharic"):
            for b in comp_blogs:
                string+=b.tag_am+","
        else:
            for b in comp_blogs:
                string+=b.tag+","
        string = string[:-1]
        tag_list = string.split(',')
        tag_list = set(tag_list)
        return tag_list

class CompanyBlogDetail(View):
    def get(self, *args, **kwargs):
        blog = Blog.objects.get(id = self.kwargs['pk'])
        comment = BlogCommentForm
        tags = get_tags("research", blog.company)
        tags_am = get_tags("amharic", blog.company)
        context = {'obj':blog, "comment":comment, 'tags':tags, 'tags_am':tags_am, 'object':blog.company}
        return render(self.request, "frontpages/company/company_blog_detail.html", context)


class CompanyBlogSearch(ListView):
        model = Blog
        template_name = "frontpages/company/company_blog.html"
        paginate_by = 2
        def get_queryset(self):
            return Blog.objects.filter( company = Company.objects.get(id = self.kwargs['pk']), tag__icontains = self.kwargs['tag'] , publish=True)
        
        def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(**kwargs)
            context['object'] = Company.objects.get(id = self.kwargs['pk'])
            if context['object_list'].count() == 0:
                context['message'] = "No result Found for the tag"
                context['object_list'] = Blog.objects.filter( company = Company.objects.get(id = self.kwargs['pk']))
            return context


class CompanyBlogCreateComment(View):
    def post(self, *args, **kwargs):
        form = BlogCommentForm(self.request.POST)
        blog = Blog.objects.get(id = self.kwargs['pk'])
        if form.is_valid():
            blogComment = BlogComment(blog = blog, created_by = self.request.user, content=form.cleaned_data.get('content'))
            blogComment.save()
            return redirect(reverse("company_blog_detail", kwargs={'pk':blog.id}))
        return redirect(reverse("company_blog_detail", kwargs={'pk':blog.id}))
            


class CompanyPollList(ListView):
    model = PollsQuestion
    template_name = "frontpages/company/company_poll.html"
    paginate_by = 2
    def get_queryset(self):
        try:
            return PollsQuestion.objects.filter(company = Company.objects.get(id = self.kwargs['pk']))
        except Exception as e:
            print( "####### Exception while gettng company events ",e)
            return []
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
        

class CompanyFaq(ListView):
    model = Faqs
    template_name = "frontpages/company/company_faq.html"
    paginate_by = 2
    def get_queryset(self):
        return Faqs.objects.filter( company = Company.objects.get(id = self.kwargs['pk']), status='APPROVED' )
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = Company.objects.get(id = self.kwargs['pk'])
        if context['object_list'].count() == 0:
            context['message']  = "No APPROVED Faqs found for this coompany!"
        return context


class CompanyFaqDetail(View):
    def get(self, *args, **kwargs):
        faq = Faqs.objects.get(id=self.kwargs['pk'])
        return render(self.request, "frontpages/company/company_faq_detail.html", {'obj':faq, 'object':faq.company})
    
