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
from django.db import IntegrityError
# 
from product import models
from product.models import *
from accounts.models import UserProfile
from company.models import Company,CompanyEvent, HomePageSlider, InvestmentProject
from admin_site.models import *

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm

from collaborations.models import *
from admin_site.decorators import company_created,company_is_active


# INDEX VIEW
decorators = [never_cache, company_created(),company_is_active()]
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
        record_activity(self.request.user,"PollsQuestion","Created Polls",poll.id,before=None,after=None)
        messages.success(self.request,"Poll was Successfully Created!")
        return redirect("admin:admin_polls")
    def form_invalid(self, form):
        return render(self.request, template_name, {'form': form} )


@method_decorator(decorators,name='dispatch')
class DetailPoll(LoginRequiredMixin, DetailView):
    model = PollsQuestion
    template_name = "admin/poll/admin_poll_detail.html"
    context_object_name  = "poll"

@method_decorator(decorators,name='dispatch')
class AddChoice(LoginRequiredMixin, CreateView):
    model = Choices
    form_class = CreateChoiceForm
    template_name = 'admin/poll/add_choice.html'
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        print("the first one")
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
                record_activity(self.request.user,"Choices","Added New Poll Choices",poll.id,before=None,after=None)
                messages.success(self.request,"Choice Successfully Created!")
                return redirect("admin:admin_polls")
            else:
                messages.warning(self.request, "Error! Choice Creation Failed! form case! " )
                return render(self.request, 'admin/poll/add_choice.html', {'form': form,'poll':poll})
        except Exception as e:
            print("Exception at add choice post ",e)
            return redirect('admin:admin_polls', )

    
@method_decorator(decorators,name='dispatch')
class EditPoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
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
        try:
            poll.title=self.request.POST['title']
            poll.title_am=self.request.POST['title_am']
            poll.description=self.request.POST["description"]
            poll.description_am=self.request.POST['description_am']
            poll.last_updated_by =self.request.user
            poll.last_updated_date = timezone.now()
            poll.save()
            record_activity(self.request.user,"PollsQuestion","Edited a Polls Object",poll.id,before=None,after=None)
            messages.success(self.request,"Poll has been Edited Successfully!")
            return redirect("admin:admin_polls")
        except Exception as e:
            return render(self.request, 'admin/poll/create_poll.html', {'pollform':form, 'choiceform':CreateChoiceForm, 'poll':poll, 'edit':True})

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
            choice.choice_name=self.request.POST['choice_name']
            choice.choice_name_am=self.request.POST['choice_name_am']
            choice.description=self.request.POST["description"]
            choice.description_am=self.request.POST['description_am']
            choice.last_updated_by=self.request.user
            choice.last_updated_date=timezone.now()
            choice.save()
            record_activity(self.request.user,"Choices","Poll Choices Updated",choice.id)
            messages.success(self.request,"Choice has been Edited Successfully!")
            return redirect("admin:admin_polls")

        except Exception as e:
                print("error at Edit poll post", str(e))
                messages.warning(self.request, "Error! Choice was not Edited!" )
                return render(self.request,'admin/poll/add_choice.html',{ 'choiceform':CreateChoiceForm, 'choice':choice, 'edit':True})
        
def record_activity(user,model_name,activity,object_id,before=None,after=None):
    try:
        UserActivityLog.objects.create(
            user=user,
            object_id=object_id,
            model_name=model_name,
            before_change=before,
            after_change=after,
            activity=activity
        )
        return True
    except Exception as e:
        print(e)
        return False

def visitor_ip_address(request):
    x_forwarded_for= request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def record_visit(request):
    try:
        UserTracker.objects.create(ipaddress=visitor_ip_address(request))
        return True
    except IntegrityError as e:
        return False