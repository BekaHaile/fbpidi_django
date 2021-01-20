from collaborations.models import Blog, BlogComment
from collaborations.forms import CreateBlogComment
from collaborations.forms import CreateFaqs
from collaborations.models import Faqs
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import PollsQuestion, Choices, PollsResult, Tender, TenderApplicant, TenderApplications
from .forms import PollsForm, TenderForm, TenderEditForm
from django.contrib import messages
from company.models import Company, CompanyBankAccount, Bank
from accounts.models import User, CompanyAdmin, Company
import os
from django.http import FileResponse
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


import mimetypes


#blog-grid-right 
class BlogList(View):

    def get(self,*args,**kwargs):
        blog = Blog.objects.filter(publish=True) 
        template_name="frontpages/blog-grid-right.html"
        context={'blogs':blog}
        return render(self.request, template_name,context)


class BlogDetail(View):

	def get(self,*args,**kwargs):
		blog = Blog.objects.get(id=self.kwargs['id'])
		comment = CreateBlogComment()
		template_name="frontpages/blog-details-right.html" 
		context = {'blog':blog,'comment':comment}
		return render(self.request, template_name,context)
	def post(self,*args,**kwargs):
		form = CreateBlogComment(self.request.POST)
		blog = Blog.objects.get(id=self.kwargs['id'])
		template_name="frontpages/blog-details-right.html" 
		if form.is_valid():
			blogComment=BlogComment(blog=blog,
				sender=self.request.user,
				content=self.request.POST['content'])
			blogComment.save()
			comment = CreateBlogComment()
			context = {'blog':blog,'comment':comment}
			return render(self.request, template_name,context)


class FaqList(View):
	def get(self,*args,**kwargs):
		template_name="frontpages/faq.html"
		faq = Faqs.objects.all()
		context = {'faqs':faq}
		return render(self.request, template_name,context)


class PollIndex(View):
    def get(self, *args, **kwargs):
        context = {}
        polls = PollsQuestion.objects.all()
        context={'polls':polls}
        return render(self.request, "frontpages/polls-list.html", context)

       

#only visible to logged in and never voted before
class PollDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        message = ""
        context = {}        
        if self.kwargs['id'] :
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                context ['poll'] = poll
                if poll.pollsresult_set.filter(user = self.request.user).count() > 0:
                    context ['has_voted'] = True

                return render(self.request, "frontpages/poll_detail.html", context)

            except Exception as e:
                print ("444444444444444444444444" ,str(e))
                messages.error(self.request, "Poll not found")
                return redirect("polls") 

        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("polls")

    def post(self,*args,**kwargs):
        if self.kwargs['id'] and self.request.POST['selected_choice']: 
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id'] )

                # if the creator tries to vote, redirect to poll list
                # if poll.user == self.request.user:
                #     messages.error(self.request, "You can not vote on this poll, since you are the creator of the poll!")
                #     return redirect("polls") 
                
                # # #if the user already voted on this poll, redirect to poll list
                # if PollsResult.objects.filter(poll=poll, user = self.request.user):
                #     messages.error(self.request, "You have already voted for on poll!")
                #     return redirect("polls") 
                
                vote = PollsResult(
                    poll = poll,
                    user = self.request.user,
                    choice = Choices.objects.get(id = self.request.POST['selected_choice']),
                    remark=self.request.POST['remark']
                )

                vote.save()
                messages.success(self.request, "Successfully voted!")
                return redirect("polls") 

            except Exception as e:
                messages.error(self.request, "Poll not found!")
                return redirect("polls") 
             
                
        messages.error(self.request, "Invalid Vote!")        
        return redirect("polls")
        



########## tender related views
###
class CreateTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:    
            form = TenderForm()
            company = Company.objects.filter(user = self.request.user).first()
            company_bank_accounts = company.get_bank_accounts()
            banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
            
            context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts}
            return render(self.request,'admin/collaborations/create_tender.html',context)
        except Exception:
            return redirect("admin:polls")
    
    def post(self,*args,**kwargs):
        form = TenderForm(self.request.POST)  
        try:                 
            if form.is_valid():
                print("form is valid")
                tender = form.save(commit=False)
                user = None
                if self.request.user.is_company_admin: 
                    user = CompanyAdmin.objects.get(user=self.request.user) 

                # elif self.request.user.is_staff:
                #     user = CompanyStaff.objects.get(user.self.request.user)
                tender.user = self.request.user
                if  self.request.FILES['document']:
                    tender.document = self.request.FILES['document']
                
                tender.save()
                tender.bank_account.add(self.request.POST['company_bank_account'])
                
                messages.success(self.request,"Tender Successfully Created")
                return redirect("admin:tenders")
                
            else:
                import pprint
                
                pprint.pprint(self.request.POST)
                print("2")
                pprint.pprint(self.request.FILES)
                print(form.errors)
                messages.error(self.request, "Error! Poll was not Created!" )
                return redirect("admin:tenders")
                
        except Exception as e:
            print("Exception at collaborations.views.CreateTender post" , str (e))
            return redirect("admin:tenders")


class TenderList(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):          
        try:
                tenders = Tender.objects.all()
                return render(self.request, "admin/collaborations/tenders.html", {'tenders':tenders,})
        except Exception as e:
                messages.error(self.request, "Error while getting tenders")
                return redirect("admin:tenders") 


class TenderDetail(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):         
        form = TenderForm()
        if self.kwargs['id']:
            try:
                tender = Tender.objects.get(id =self.kwargs['id'] )
                company = tender.get_company()
                company_bank_accounts = company.get_bank_accounts()
                context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts, 'tender':tender}
                return render(self.request,'admin/collaborations/tender_detail.html',context)
            except Exception as e:
                print(str(e))
                messages.error(self.request,"Tender  edit error")
                return redirect("admin:tenders")

        print("error at tenderDetail for admin")
        return redirect("admin:tenders")



class AddTenderBankAccount(LoginRequiredMixin,View):
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
            return redirect("admin:tenders")

        else:
            messages.error(self.request, "Error! Choice Creation Failed! form case! " )
            return redirect("admin:tenders")


class EditTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        
        form = TenderForm()
        company = Company.objects.filter(user = self.request.user).first()
        company_bank_accounts = company.get_bank_accounts()
        banks= Bank.objects.all() # if there will be a scenario where the admin needs to add register new bank account
        
        context = {'form':form, 'banks':banks, 'company_bank_accounts':company_bank_accounts}
        
        if self.kwargs['id']:
            try:
                tender = Tender.objects.get(id =self.kwargs['id'] )
                context['tender'] = tender 
                context['edit'] = True
                return render(self.request,'admin/collaborations/create_tender.html',context)
            except Exception as e:
                print(str(e))
                messages.error(self.request,"Tender  edit error")
                return redirect("admin:tenders")

        return render(self.request,'admin/collaborations/create_tender.html',context)

    def post(self,*args,**kwargs):

        print("Edit tender")
        
        form = TenderEditForm(self.request.POST)  
        try:                 
            if form.is_valid():
                import pprint
                
                pprint.pprint(self.request.POST)
                print("2")
                pprint.pprint(self.request.FILES)
                print(form.errors)
                print("form is valid")
                tender= Tender.objects.get(id = self.kwargs['id'])
                message = []
                
                if self.request.FILES['document'] != "":
                    tender.document = self.request.FILES['document'] 
                if self.request.POST['start_date']  != "":
                    try:
                        tender.start_date = self.request.POST['start_date']
                    except Exception:
                        message.append("Start date Error")

                if self.request.POST['end_date']  != "":
                    try:
                        tender.start_date = self.request.POST['end_date']
                    except Exception:
                        message.append("end date Error")
                
                tender.title = form.cleaned_data.get('title')
                tender.title_am = form.cleaned_data.get('title_am')
                tender.description = form.cleaned_data.get('description')
                tender.description_am = form.cleaned_data.get('description_am')
                tender.type = form.cleaned_data.get('tender_type')
                tender.status = form.cleaned_data.get("status")
                tender.save()
                
                messages.success(self.request,"Tender Successfully Created")
                return redirect("admin:tenders")
                
            else:
                import pprint
                
                pprint.pprint(self.request.POST)
                print("2")
                pprint.pprint(self.request.FILES)
                print(form.errors)
                messages.error(self.request, "Error! Poll was not Created!" )
                return redirect("admin:tenders")
                
        except Exception as e:
            print("Exception at collaborations.views.editTender post" , str (e))
            return redirect("admin:tenders")
       
       
class DeleteTender(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            tender = Tender.objects.filter(id = self.kwargs['id']  )
            if tender:
                tender.delete()
                message = "Tender Deleted Successfully"
                messages.success(self.request,message)
                return redirect("admin:tenders")
            else:
                messages.error(self.request, "NO such tender was found!")
                return redirect("admin:tenders")


        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("admin:tenders")


######## Tender for customers
class CustomerTenderList(View):
    def get(self, *args, **kwargs):          
        try:
                tenders = Tender.objects.all()
                return render(self.request, "frontpages/tender/customer_tender_list.html", {'tenders':tenders,})
        except Exception as e:
                messages.error(self.request, "Error while getting tenders")
                return redirect("polls")     



class CustomerTenderDetail(View):
    def get(self, *args, **kwargs):  
          
        if self.kwargs['id'] :
            try:
                tender = Tender.objects.get(id = self.kwargs['id']  )
                return render(self.request, "frontpages/tender/customer_tender_detail.html", {'tender':tender,})

            except Exception as e:
                print("eeeeeeeeeeeeeeeee", str(e))
                messages.error(self.request, "tender not found")
                return redirect("tender_list") 

        else:

            messages.error(self.request, "Nothing selected!")
            return redirect("tender_list")




# def DownloadDocument(request):
#     # fill these variables with real values
#     file_path = tender.document.path
#     filename = tender.document.name

#     fl = open(fl_path, 'r' )
#     mime_type, _ = mimetypes.guess_type(file_path)
#     response = HttpResponse(fl, content_type=mime_type)
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     return response



# class DownloadDocument(View):
#     def get(self, *args, **kwargs):
#         print("downloading")
#         try:
#             file_path = tender.document.path
#             filename = tender.document.name

#             fl = open(fl_path, 'r' )
#             mime_type, _ = mimetypes.guess_type(file_path)
#             response = HttpResponse(fl, content_type=mime_type)
#             response['Content-Disposition'] = "attachment; filename=%s" % filename
#             return redirect('tender_list')
#         except Exception as e:
#             print(str(e))
#             return redirect('tender_list')


        # return redirect(f"/collaborations/customer_tender_detail/{tender.id}/")