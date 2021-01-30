from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import os

# 
from product import models
from accounts.models import User
from company.models import Company,CompanyEvent



from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm
from collaborations.models import PollsQuestion, PollsResult, Choices,Faqs, Vacancy, JobCategoty, Blog, Announcement, ForumComments, CommentReplay, News, NewsImages
from django.http import HttpResponse, FileResponse
 
# 


# INDEX VIEW
class AdminIndex(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            context = dict()
            return render(self.request,"admin/index.html",context)
        except Exception as e:
            print ("index error",str(e))
            return render(self.request,"admin/index.html",context)


class DeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['model_name'] == 'category':
            category = models.Category.objects.get(id=self.kwargs['id']) 
            category.delete()
            message = "Category Deleted"
            messages.success(self.request,message)
            return redirect("admin:p_categories",option='category')
        elif self.kwargs['model_name'] == 'Vacancy':
            vacancy = Vacancy.objects.get(id=self.kwargs['id'])
            vacancy.delete()
            message ="Vacancy Deleted"
            messages.success(self.request,message)
            if self.request.user.is_superuser:
                return redirect("admin:super_Job_list")
            return redirect("admin:Job_list")
        elif self.kwargs['model_name'] == 'ForumComments':
            announcement = ForumComments.objects.get(id=self.kwargs['id'])
            announcement.delete()
            return redirect("forum_list")
        elif self.kwargs['model_name'] == 'CommentReplay':
            commentreplay = CommentReplay.objects.get(id=self.kwargs['id'])
            commentreplay.delete()
            return redirect("forum_list")
        elif self.kwargs['model_name'] == 'Announcement':
            announcement = Announcement.objects.get(id=self.kwargs['id'])
            announcement.delete()
            message ="Announcement Deleted"
            messages.success(self.request,message)
            return redirect("admin:anounce_list")
        elif self.kwargs['model_name'] == 'JobCategoty':
            jobcategory = JobCategoty.objects.get(id=self.kwargs['id'])
            jobcategory.delete()
            message ="Job category Deleted"
            messages.success(self.request,message)
            return redirect("admin:admin_jobcategoty")
        elif self.kwargs['model_name'] == 'Blog':
            Blog1 = Blog.objects.get(id=self.kwargs['id'])
            Blog1.delete()
            message ="Blog Deleted"
            messages.success(self.request,message)
            return redirect("admin:admin_Blogs")
        elif self.kwargs['model_name'] == 'Faqs':
            faqs = Faqs.objects.get(id=self.kwargs['id'])
            faqs.delete()
            message ="Faqs Deleted"
            messages.success(self.request,message)
            return redirect("admin:admin_Faqs") 
        elif self.kwargs['model_name'] == 'sub_category':
            sub_category = models.SubCategory.objects.get(id=self.kwargs['id'])
            sub_category.delete()
            message ="Sub-Category Deleted"
            messages.success(self.request,message)
            return redirect("admin:p_categories",option='sub_category')
        elif self.kwargs['model_name'] == 'user_account':
            user = User.objects.get(id=self.kwargs['id'])
            user.delete()
            message ="User Deleted"
            messages.success(self.request,message)
            return redirect("admin:users_list")
        elif self.kwargs['model_name'] == 'product':
            product = models.Product.objects.get(id=self.kwargs['id'])
            product.delete()
            message ="Product Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'company':
            company = Company.objects.get(id=self.kwargs['id'])
            company.delete()
            message ="Company Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'product_image':
            pdimage = models.ProductImage.objects.get(id=self.kwargs['id'])
            pdimage.delete()
            message ="Image Deleted"
            messages.success(self.request,message)
            return redirect("admin:product_detail",id=pdimage.product.id,option='view')
        elif self.kwargs['model_name'] == 'News':
            try:
                news = News.objects.get(id = self.kwargs['id']  )
                news.delete() 
                messages.success(self.request,"News Deleted Successfully")
                return redirect("admin:news_list")
            except Exception as e:
                messages.warning(self.request, "Could not find the News")
                return redirect("admin:news_list")
           
        elif self.kwargs['model_name'] == "NewsImage":
            try:  
                image = NewsImages.objects.get(id = self.kwargs['id']  )
                news = image.news
                image.delete()
                messages.success(self.request,"Image Deleted Successfully!")
                return redirect(f"/admin/edit_news/{news.id}")
            except Exception as e:
                messages.warning(self.request, "Could not find the Image")
                return redirect("admin:news_list")
        elif self.kwargs['model_name'] == 'CompanyEvent':
            try:  
                
                event = CompanyEvent.objects.get(id = self.kwargs['id']  )
                company = event.company
                event.delete()
                messages.success(self.request,"Event Deleted Successfully!")
                return redirect("admin:view_fbpidi_company") if event.company.company_type == "fbpidi" else redirect("admin:view_company_profile")

            except Exception as e:
                messages.warning(self.request, "Could not find the Event")
                return redirect("admin:view_fbpidi_company") if event.company.company_type == "fbpidi" else redirect("admin:view_company_profile")
                
class Polls(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = PollsForm()
        polls = PollsQuestion.objects.all()
        context = {'form':form, 'polls':polls}
        
        return render(self.request,'admin/pages/polls.html',context)
    
   
class CreatePoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):

        form = CreatePollForm()
        context = {'form':form}
        return render(self.request,'admin/pages/create_poll.html',context)
    
    def post(self,*args,**kwargs):
        
        form = CreatePollForm(self.request.POST)  
        try:      
            if form.is_valid():
                poll = PollsQuestion(
                    user=self.request.user,
                    title=form.cleaned_data.get('title'),
                    title_am=form.cleaned_data.get('title_am'),
                    description=form.cleaned_data.get("description"),
                    description_am=form.cleaned_data.get('description_am'),
                    
                )
                poll.save()
                messages.success(self.request,"Poll was Successfully Created!")
                return redirect("admin:admin_polls")
            else:
                messages.warning(self.request, "Error! Poll was not Created!" )
                return redirect("admin:admin_polls")
                
        except Exception as e:
            print("44444444444444444444" , str (e))
            return redirect("admin:admin_polls")


class DetailPoll(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):  
          
        if self.kwargs['id'] :
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                # return render(self.request, "admin/pages/company_detail.html", {'poll':poll,})
                return render(self.request, "admin/pages/admin_poll_detail.html", {'poll':poll,})

            except Exception as e:
                print("eeeeeeeeeeeeeeeee", str(e))
                messages.warning(self.request, "Poll not found")
                return redirect("admin:admin_polls") 

        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")

class AddChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
        
        form = CreateChoiceForm()
        context = {'form':form, 'poll':poll}
        return render(self.request,'admin/pages/add_choice.html',context)
    
    def post(self,*args,**kwargs):
        form = CreateChoiceForm(self.request.POST)
        
        poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
        if form.is_valid():
            choice = Choices(
                choice_name=form.cleaned_data.get('choice_name'),
                choice_name_am=form.cleaned_data.get('choice_name_am'),
                description=form.cleaned_data.get("description"),
                description_am=form.cleaned_data.get('description_am'),     
            )
            choice.save()

            poll.choices.add(choice)
            poll.save()
            print(poll.choices.all())
            
            messages.success(self.request,"Choice Successfully Created!")
            return redirect("admin:admin_polls")

        else:
            messages.warning(self.request, "Error! Choice Creation Failed! form case! " )
            return redirect("admin:admin_polls")


class EditPoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        pollform = CreatePollForm()
        choiceform = CreateChoiceForm()
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
            # little verification (this verification is done at the front end, this is just for safety, like if user uses url)            
            if poll.count_votes() != 0:
                messages.warning(self.request, "Couldn't Edit poll, because poll Edit has started!")
                return redirect('admin:admin_polls')
            context = {'pollform':pollform, 'choiceform':choiceform, 'poll':poll}
            context['edit'] = True
        except Exception as e:          
            print(str(e))
            messages.warning(self.request, "Error, Couldn't Edit poll!")
            return redirect('admin:admin_polls')
        return render(self.request,'admin/pages/create_poll.html',context)

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
        poll.save()
        messages.success(self.request,"Poll has been Edited Successfully!")
        return redirect("admin:admin_polls")
       
class EditChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):        
        choiceform = CreateChoiceForm()
        
        try:
            choice = Choices.objects.get(id = self.request.GET['choice'][0] )
            context = { 'choiceform':choiceform, 'choice':choice}
            context['edit'] = True
            
        except Exception as e:
    
            print(str(e))
            messages.warning(self.request, "Error, Couldn't Edit Choice!")
            return redirect('admin:admin_polls')
    
        return render(self.request,'admin/pages/add_choice.html',context)

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
        choice.save()
        messages.success(self.request,"Choice has been Edited Successfully!")
        return redirect("admin:admin_polls")
       
class DeletePoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            poll = PollsQuestion.objects.filter(id = self.kwargs['id']  )
            if poll:
                poll.delete()
                message = "Poll Deleted Successfully"
                messages.success(self.request,message)
                return redirect("admin:admin_polls")
            else:
                messages.warning(self.request, "NO such poll was found!")
                return redirect("admin:admin_polls")


        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")

class DeleteChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            choice = Choices.objects.filter(id = self.kwargs['id']  )
            if choice:
                choice.delete()
                message = "Choice Deleted Successfully"
                messages.success(self.request, message)
                return redirect("admin:admin_polls")
            else:
                messages.warning(self.request, "NO such Choice was found!")
                return redirect("admin:admin_polls")


        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")