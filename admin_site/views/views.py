import os
from django.utils import timezone
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.db.models import Q

# 
from product import models
from product.models import *
from accounts.models import UserProfile
from company.models import Company,CompanyEvent, HomePageSlider, InvestmentProject
from admin_site.models import *
from chat.models import ChatGroup, ChatMessage

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm

from collaborations.models import *
from admin_site.decorators import company_created

# 
# INDEX VIEW
decorators = [never_cache, company_created()]
@method_decorator(decorators,name='get')
class AdminIndex(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        return render(self.request,"admin/index.html",{'title':'FBP-IIMS'})

@method_decorator(decorators,name='dispatch')
class Polls(LoginRequiredMixin, ListView):
    context_object_name = 'polls'
    model = PollsQuestion
    template_name = 'admin/poll/polls.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PollsQuestion.objects.all()
        else:
            return PollsQuestion.objects.filter(company=self.request.user.get_company())
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = PollsForm
        return context

@method_decorator(decorators,name='dispatch')
class CreatePoll(LoginRequiredMixin, CreateView):
    model = PollsQuestion
    form_class = CreatePollForm
    template_name  = 'admin/poll/create_poll.html'
    template_name_suffix = '_create_form'
    success_url = "/admin/polls/"

    def form_valid(self, form):
        poll = form.save(commit=False)
        poll.created_by = self.request.user
        poll.save()
        messages.success(self.request,"Poll was Successfully Created!")
        return redirect("admin:admin_polls")



# class CreatePoll(LoginRequiredMixin,View):
#     def get(self,*args,**kwargs):
#         check_user_has_company(self.request.user)
#         return render(self.request,'admin/poll/create_poll.html',{'form':CreatePollForm})
#     def post(self,*args,**kwargs):
#         form = CreatePollForm(self.request.POST)  
#         try:      
#             if form.is_valid():
#                 poll =form.save(commit=False)
#                 poll.created_by = self.request.user
#                 poll.save()
#                 messages.success(self.request,"Poll was Successfully Created!")
#                 return redirect("admin:admin_polls")
#             else:
#                 messages.warning(self.request, "Error! Poll was not Created!" )
#                 return redirect("admin:admin_polls")    
#         except Exception as e:
#             print("there is an exception", e)
#             return redirect("admin:admin_polls")

@method_decorator(decorators,name='dispatch')
class DetailPoll(LoginRequiredMixin, DetailView):
    model = PollsQuestion
    template_name = "admin/poll/admin_poll_detail.html"
    context_object_name  = "poll"

    # def get(self, *args, **kwargs):  
    #     if self.kwargs['id'] :
    #         try:
    #             poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
    #             return render(self.request, , {'poll':poll,})

    #         except Exception as e:
    #             print("exception while showing poll Detail", str(e))
    #             messages.warning(self.request, "Poll not found")
    #             return redirect("admin:admin_polls") 

    #     else:
    #         messages.warning(self.request, "Nothing selected!")
    #         return redirect("admin:admin_polls")


# class AddChoice(LoginRequiredMixin, CreateView):
#     model = Choices
#     form_class = CreateChoiceForm
#     template_name = 'admin/poll/add_choice.html'
#     template_name_suffix  = '_create_form'

#     def form_valid(self, form):
#         try:
#             poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
#             choice = form.save(commit=False)
#             choice.created_by = self.request.user
#             choice.save()
#             poll.choices.add(choice)
#             poll.save()
#             messages.success(self.request,"Choice Successfully Created!")
#             return redirect("admin:admin_polls")

#         except Exception as e:
#             print("Poll not found ", e)

@method_decorator(decorators,name='dispatch')
class AddChoice(LoginRequiredMixin, CreateView):
    model = Choices
    form_class = CreateChoiceForm
    template_name = 'admin/poll/add_choice.html'
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['poll']  = PollsQuestion.objects.get(id = self.kwargs['id'] )
        return context
        


@method_decorator(decorators,name='dispatch')
class AddChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
            return render(self.request,'admin/poll/add_choice.html',{'form':CreateChoiceForm, 'poll':poll})
        except Exception as e:
            print("Exception at  add choice ", e)
            return redirect('admin:admin_polls')
    
    def post(self,*args,**kwargs):
        form = CreateChoiceForm(self.request.POST)
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
            if form.is_valid():
                choice = form.save(commit=False)
                choice.created_by = self.request.user
                choice.save()
                poll.choices.add(choice)
                poll.save()
                messages.success(self.request,"Choice Successfully Created!")
                return redirect("admin:admin_polls")
            else:
                messages.warning(self.request, "Error! Choice Creation Failed! form case! " )
                return redirect("admin:admin_polls")
        except Exception as e:
            print("Exception at add choice post ",e)
            return redirect('admin:admin_polls')


# class EditPoll(LoginRequiredMixin, UpdateView):
#     model = PollsQuestion
#     form_class = CreatePollForm
#     template_name = "admin/poll/create_poll.html"
#     template_name_suffix = '_update_form'
#     context_object_name = 'poll'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['edit'] = True
#         return context
        
#     def form_valid(self, form):
#         poll = form.save(commit = False)
#         poll.last_updated_by = self.request.user
#         poll.last_updated_date = timezone.now()
#         poll.save()
#         messages.success(self.request,"Poll has been Edited Successfully!")
#         return redirect("admin:admin_polls")

    
@method_decorator(decorators,name='dispatch')
class EditPoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
            # little verification (this verification is done at the front end, this is just for safety, like if user uses url)            
            if poll.count_votes() != 0:
                messages.warning(self.request, "Couldn't Edit poll, because poll Edit has started!")
                return redirect('admin:admin_polls')
            return render(self.request,'admin/poll/create_poll.html', {'pollform':CreatePollForm, 'choiceform':CreateChoiceForm, 'poll':poll, 'edit':True})
        except Exception as e:          
            print("Exception at Edit poll ",str(e))
            messages.warning(self.request, "Error, Couldn't Edit poll!")
            return redirect('admin:admin_polls')

    def post(self,*args,**kwargs):
        form = CreatePollForm(self.request.POST)     
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'])
        except Exception as e:
                print("error at Editpoll post", str(e))
                messages.warning(self.request, "Error! Poll was not Edited!" )
                return redirect("admin:admin_polls")
        poll.title=self.request.POST['title']
        poll.title_am=self.request.POST['title_am']
        poll.description=self.request.POST["description"]
        poll.description_am=self.request.POST['description_am']
        poll.last_updated_by =self.request.user
        poll.last_updated_date = timezone.now()
        poll.save()
        messages.success(self.request,"Poll has been Edited Successfully!")
        return redirect("admin:admin_polls")

@method_decorator(decorators,name='dispatch')
class EditChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):        
        try:
            choice = Choices.objects.get(id = self.request.GET['choice'][0] )
            return render(self.request,'admin/poll/add_choice.html',{ 'choiceform':CreateChoiceForm, 'choice':choice, 'edit':True})
        except Exception as e:
            print( "Exception at Editchoice get  ",str(e))
            messages.warning(self.request, "Error, Couldn't Edit Choice!")
            return redirect('admin:admin_polls')
        
    def post(self,*args,**kwargs):
        form = CreateChoiceForm(self.request.POST)       
        try:
            choice = Choices.objects.get(id = self.request.POST['choice'])
        except Exception as e:
                print("error at Editpoll post", str(e))
                messages.warning(self.request, "Error! Choice was not Edited!" )
                return redirect("admin:admin_polls")  
        choice.choice_name=self.request.POST['choice_name']
        choice.choice_name_am=self.request.POST['choice_name_am']
        choice.description=self.request.POST["description"]
        choice.description_am=self.request.POST['description_am']
        choice.last_updated_by=self.request.user
        choice.last_updated_date=timezone.now()
        choice.save()
        messages.success(self.request,"Choice has been Edited Successfully!")
        return redirect("admin:admin_polls")
    
  
