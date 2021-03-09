import datetime

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views.generic import CreateView,UpdateView,ListView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone

from company.models import (Company,CompanySolution,CompanyEvent,
                            CompanyStaff, Bank, CompanyBankAccount,
                            InvestmentCapital)
from accounts.models import CompanyAdmin,User
from product.models import Order,OrderProduct



from company.forms import (CompanyForm,CompanyProfileForm,CompanyDetailForm,CompanySolutionForm,
                            CompanyEventForm,FbpidiCompanyForm,InvestmentCapitalForm,
                         CompanyBankAccountForm, EventParticipantForm)
from chat.models import ChatGroup, ChatMessage

class CreateMyCompanyProfile(LoginRequiredMixin,CreateView):
    model=Company
    form_class = CompanyProfileForm
    template_name = "admin/company/create_company_form.html"

    def form_valid(self,form):
        company = form.save(commit=False)
        company.contact_person = self.request.user
        company.craeted_by = self.request.user
        company.save()
        messages.success(self.request,"Company Profile Created")
        return redirect("admin:create_company_detail",pk=company.id)

class CreateCompanyDetail(LoginRequiredMixin,UpdateView):
    model = Company
    form_class = CompanyDetailForm
    template_name = "admin/company/create_company_detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['inv_capital_form'] = InvestmentCapitalForm
        return context

    def form_valid(self,form):
        company = form.save(commit=False)
        company.last_updated_by = self.request.user
        company.last_updated_date = timezone.now()
        company.save()
        messages.success(self.request,"Company Detail Information Added")
        return redirect("admin:index")

class CreateInvestmentCapital(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        print(self.request.POST['formData'])
        return JsonResponse({"DATA!"})

        

class CreateCompanyProfile(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        form = CompanyForm()
        try:
            Company.objects.get(user=self.request.user)
            return redirect("admin:view_company_profile")
        except:
            return render(self.request,"admin/company/company_form_create.html",{"form":form})

    def post(self, *args,**kwargs):
        form = CompanyForm(self.request.POST,self.request.FILES)
        
        if form.is_valid():
            company = form.save(commit=False)
            company.product_category = form.cleaned_data.get("product_category")
            company.user = self.request.user
            company.save()
            messages.success(self.request,"Company Profile Created")
            return redirect("admin:index")
        return render(self.request,"admin/company/company_form_create.html",{'form':form})


class CreateCompanyProfileAfterSignUp(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        form = CompanyForm()
        try:
            Company.objects.get(user=self.request.user)
            return redirect("admin:view_company_profile")
        except:
            return render(self.request,"admin/company/company_form_signup.html",{"form":form})

    def post(self, *args,**kwargs):
        form = CompanyForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.product_category = form.cleaned_data.get("product_category")
            company.user = self.request.user
            company.save()
            messages.success(self.request,"Company Profile Created")
            return redirect("admin:index")
        return render(self.request,"admin/company/company_form_signup.html",{'form':form})


class ViewCompanyProfile(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        company = None
        try:
            if self.request.user.is_company_admin:
                company = Company.objects.get(user=self.request.user)
            if self.request.user.is_company_staff:
                comp_staff = CompanyStaff.objects.get(user = self.request.user)
                company = Company.objects.get(id=comp_staff.company.id)
            sol_form = CompanySolutionForm()
            staff_users = CompanyStaff.objects.filter(company=company)
            solutions = CompanySolution.objects.filter(company=company)
            events = CompanyEvent.objects.filter(company=company)
            event_form = CompanyEventForm
            banks = Bank.objects.all()
            company_bank_accounts = CompanyBankAccount.objects.filter(company=company)
            account_form = CompanyBankAccountForm()

            context = {'company':company,'staff_users':staff_users,'solution_form':sol_form,'solutions':solutions,
                        'event_form':event_form,'events':events, 
                        'banks':banks, 'company_bank_accounts': company_bank_accounts, 'account_form':account_form}
            if "active_tab" in self.kwargs:#to activate a specific tab while opening the company profile, first used for message (inbox tab)
                context ['active_tab'] = self.kwargs['active_tab']
                   
            return render(self.request,'admin/company/company_profile_detail.html',context)
        except ObjectDoesNotExist:
            return redirect("admin:create_company_profile")
        
    def post(self,*args,**kwargs):
        try:
            company = Company.objects.get(id=self.kwargs['id'])
            # for company profile
            if self.request.POST['flag'] == "profile":
                company.company_name = self.request.POST['company_name']
                company.company_name_am = self.request.POST['company_name_am']
                company.location = self.request.POST['location']
                company.city = self.request.POST['city']
                company.phone_number = self.request.POST['phone_number']
                company.number_of_employees = self.request.POST['number_of_employees']
                company.certification = self.request.POST['certification']
                company.capital = self.request.POST['capital']
                company.established_year = self.request.POST['established_year']
                company.postal_code = self.request.POST['postal_code']
                company.detail = self.request.POST['detail']
                company.detail_am = self.request.POST['detail_am']
                company.color = self.request.POST['color']
                company.facebook_link = self.request.POST['facebook_link']
                company.twiter_link = self.request.POST['twiter_link']
                company.linkedin_link = self.request.POST['linkedin_link']
                company.google_link = self.request.POST['google_link']
                company.instagram_link = self.request.POST['instagram_link']
                company.pintrest_link = self.request.POST['pintrest_link']
                if self.request.FILES.get('company_logo') != None:
                    company.company_logo = self.request.FILES.get('company_logo')
                if self.request.FILES.get('company_intro') != None:
                    company.company_intro = self.request.FILES.get('company_intro')
            elif self.request.POST['flag'] == "trade":
                # for Company Trade capacity
                company.incoterms =  self.request.POST['incoterms']
                company.incoterms_am =  self.request.POST['incoterms_am']
                company.terms_of_payment =self.request.POST['terms_of_payment']
                company.average_lead_time =self.request.POST['average_lead_time']
                company.average_lead_time_am =self.request.POST['average_lead_time_am']
                print(self.request.POST['no_trading_staff'])
                if self.request.POST['no_trading_staff'] != None:
                    company.no_trading_staff = self.request.POST['no_trading_staff']
                if self.request.POST['export_yr'] != None:
                    company.export_yr = self.request.POST['export_yr']
                if self.request.POST['export_percentage'] != None:
                    company.export_percentage =self.request.POST['export_percentage']
                company.main_market =  self.request.POST['main_market']
                company.main_market_am = self.request.POST['main_market_am']
                company.nearest_port =  self.request.POST['nearest_port']
                company.nearest_port_am =self.request.POST['nearest_port_am']
            elif self.request.POST['flag'] == "production":
                # production capacity
                company.r_and_d_capacity =  self.request.POST['r_and_d_capacity']
                company.r_and_d_capacity_am =  self.request.POST['r_and_d_capacity_am']
                company.no_of_rnd_staff =    self.request.POST['no_of_rnd_staff']
                company.no_production_lines =    self.request.POST['no_production_lines']
                company.anual_op_value =    self.request.POST['anual_op_value']
                company.anual_op_main_products =   self.request.POST['anual_op_main_products']
                company.anual_op_main_products_am =   self.request.POST['anual_op_main_products_am']
            company.save()
            messages.success(self.request,"Company Updated")
            if self.request.user.is_superuser:
                return redirect("admin:company_detail",id=company.id)
            else:
                return redirect("admin:view_company_profile")
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company Does Not Exist")
            if self.request.user.is_superuser:
                return redirect("admin:company_detail",id=company.id)
            else:
                return redirect("admin:view_company_profile")
    
class CompaniesView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "supplier":
            suppliers = Company.objects.filter(company_type="supplier")
            context = {
                'companies':suppliers
            }
        elif self.kwargs['option'] == "manufacturer":
            manufacturers = Company.objects.filter(company_type="manufacturer")
            context = {
                'companies':manufacturers
            }
        print(context)
        return render(self.request,"admin/company/companies.html",context)

class CompaniesDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        company = ""
        context = {}
        try:
            company = Company.objects.get(id=self.kwargs['id'])
            staff_users = CompanyStaff.objects.filter(company=company)
            context = {
                'company':company,'staff_users':staff_users
            }
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company does not Exist")
            return redirect("admin:companies")
        return render(self.request,"admin/company/company_profile_detail.html",context)

class CreateCompanySolution(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanySolutionForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.company = Company.objects.get(id=self.kwargs['company_id'])
            solution.save()
            messages.success(self.request,"Services Created Successfully")
        messages.warning(self.request,form.errors)
        return redirect("admin:view_company_profile")

class CreateCompanyEvent(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        company = Company.objects.get(id=self.kwargs['company_id'])
        if form.is_valid():
            event = form.save(commit=False)
            event.company = company
            event.save()
            messages.success(self.request,"Event Created Successfully")
            if company.company_type == "fbpidi":
                return redirect("admin:view_fbpidi_company")
            else:
                return redirect("admin:view_company_profile")
        else:
            messages.warning(self.request,form.errors)
            if company.company_type == "fbpidi":
                return redirect("admin:view_fbpidi_company")
            else:
                return redirect("admin:view_company_profile")

class EditCompanyEvent(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        form = CompanyEventForm(self.request.POST,self.request.FILES)
        event = CompanyEvent.objects.get(id=self.kwargs['id']) 
        if form.is_valid():
            form.save(commit=False)
            event.title = self.request.POST['title']
            event.title_am = self.request.POST['title_am']
            event.description = self.request.POST['description']
            event.description_am = self.request.POST['description_am']

            starting_date = datetime.datetime.strptime(self.request.POST['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            print(type(starting_date))
            ending_date=datetime.datetime.strptime(self.request.POST['end_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            event.start_date = starting_date
            event.end_date = ending_date

            event.status = self.request.POST['status']
            if self.request.FILES:
                event.image = self.request.FILES['image']
            event.save() 
            messages.success(self.request,"Event Edited Successfully")
            return redirect("admin:view_fbpidi_company") if self.request.user.is_superuser else redirect("admin:view_company_profile")
            
        else:
            messages.warning(self.request,form.errors)
            return redirect("admin:view_fbpidi_company") if self.request.user.is_superuser else redirect("admin:view_company_profile")
            
class CreateFbpidiCompanyProfile(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = FbpidiCompanyForm()
        return render(self.request,"admin/company/company_form_fbpidi.html",{'form':form})

    def post(self,*args,**kwargs):
        form = FbpidiCompanyForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            fbpidi = form.save(commit=False)
            fbpidi.company_type = "fbpidi"
            fbpidi.company_type_am = "fbpidi"
            fbpidi.user=self.request.user
            fbpidi.save()
            return redirect('admin:index')
        else:
            return render(self.request,"admin/company/company_form_fbpidi.html",{'form':form})

class ViewFbpidiCompany(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        fbpidi = Company.objects.get(company_type="fbpidi")
        events = CompanyEvent.objects.all()
        event_form = CompanyEventForm
        banks = Bank.objects.all()
        company_bank_accounts = CompanyBankAccount.objects.filter(company=fbpidi)
        account_form = CompanyBankAccountForm()
        context = {'company':fbpidi,'events':events,'event_form':event_form, 'banks':banks, 'company_bank_accounts': company_bank_accounts, 'account_form':account_form}
        context['active_tab'] = 'inbox'
        # if 'active_tab' in self.kwargs:
            # print("########## Active tab is", self.kwargs['active_tab'])
            # context['active_tab'] = self.kwargs['active_tab']

        return render(self.request,"admin/company/company_profile_fbpidi.html",context)
    
    def post(self,*args,**kwargs):
        company = Company.objects.get(id=self.kwargs['id'])
        try:
            if self.request.POST['flag'] == "profile":
                company.company_name = self.request.POST['company_name']
                company.company_name_am = self.request.POST['company_name_am']
                company.location = self.request.POST['location']
                company.city = self.request.POST['city']
                company.phone_number = self.request.POST['phone_number']
                company.postal_code = self.request.POST['postal_code']
                company.established_year = self.request.POST['established_year']
                company.detail = self.request.POST['detail']
                company.detail_am = self.request.POST['detail_am']
            elif self.request.POST['flag'] == "aditional":
                company.facebook_link = self.request.POST['facebook_link']
                company.twiter_link = self.request.POST['twiter_link']
                company.linkedin_link = self.request.POST['linkedin_link']
                company.google_link = self.request.POST['google_link']
                company.instagram_link = self.request.POST['instagram_link']
                company.pintrest_link = self.request.POST['pintrest_link']
                if self.request.FILES.get('company_logo') != None:
                    company.company_logo = self.request.FILES.get('company_logo')
                if self.request.FILES.get('company_intro') != None:
                    company.company_intro = self.request.FILES.get('company_intro')
            company.save()
            messages.success(self.request,"Company Updated")
            return redirect("admin:view_fbpidi_company")
        except ObjectDoesNotExist:
            messages.warning(self.request,"Company Does Not Exist")
            return redirect("admin:view_fbpidi_company")

class CreateCompanyBankAccount(LoginRequiredMixin, View):
        def post(self, *ags, **kwargs):
            form  = CompanyBankAccountForm(self.request.POST)
            if form.is_valid:
                    account = form.save(commit=False)
                    company = Company.objects.get(id = self.kwargs['id'])
                    account.company = company
                    account.save()
                    messages.success(self.request, "New Bank Account Successfully Added!")
                    if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                    else:
                        return redirect("admin:view_company_profile")
            else:   
                messages.warning(self.request, "Error While Adding New Bank Account!")  
                company = Company.objects.get(id = self.kwargs['id'])
                if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      

class EditCompanyBankAccount(LoginRequiredMixin, View):
       
        def post(self, *ags, **kwargs):
            form  = CompanyBankAccountForm(self.request.POST)
            if form.is_valid:     
                bank_account = CompanyBankAccount.objects.get(id = self.kwargs['id'])
                bank_account.bank = Bank.objects.get(id =self.request.POST['bank'])
                bank_account.account_number = self.request.POST['account_number']
                bank_account.save()
                messages.success(self.request, "Bank Account Successfully Edited!")
                
                if bank_account.company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      

            else:   
                messages.warning(self.request, "Error While Adding New Bank Account!")  
                company = Company.objects.get(id = self.kwargs['id'])
                if company.company_type == "fbpidi":
                        return redirect("admin:view_fbpidi_company")
                else:
                        return redirect("admin:view_company_profile")      

class DeleteCompanyBankAccount(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        message = ""
        redirect_url = ""
        if self.request.user.is_superuser:
            redirect_url = "admin:view_fbpidi_company"
        else:
            redirect_url = "admin:view_company_profile"

        if self.kwargs['id'] :
            bank_account = CompanyBankAccount.objects.filter(id = self.kwargs['id']  ).first()
            
            if bank_account:
                bank_account.delete()
                message = "Bank Account Deleted Successfully"
                messages.success(self.request,message)
                
                return redirect(redirect_url)
            else:
                messages.warning(self.request, "NO such tender was found!")
                return redirect(redirect_url)


        else:
            messages.warning(self.request, "Nothing selected!")
            return redirect(redirect_url)



############## newly added, delete this commet after everything has worked right

class MnfcCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.all()
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)

class SupCompanyByMainCategory(View):
    def get(self,*args,**kwargs):
        companies = Company.objects.all()
        company_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for company in companies:
                if company.product_category.category_name.category_type == "Beverage":
                    company_list.append(company)
        elif self.kwargs['option'] == "Food":
            for company in companies:
                if company.product_category.category_name.category_type == "Food":
                    company_list.append(company)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for company in companies:
                if company.product_category.category_name.category_type == "Pharmaceuticals":
                    company_list.append(company)
        elif self.kwargs['option'] == "all":
            for company in companies:
                company_list.append(company)
        context['companies'] = company_list
        context['count'] = len(company_list)
        return render(self.request,"frontpages/company/company_list.html",context)

