# django imports
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission,Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# third party app imports
from useraudit.models import FailedLoginLog,LoginAttempt,LoginLog,UserDeactivation

from accounts.forms import (CompanyAdminCreationForm,CustomerCreationForm,CompanyUserCreationForm,
                            AdminCreateUserForm,GroupCreationForm,CompanyForm)
from accounts.models import User,Company,CompanyAdmin,CompanyStaff,Customer
from accounts.email_messages import sendEmailVerification,sendWelcomeEmail

class CompanyAdminSignUpView(CreateView):
    model = User
    form_class = CompanyAdminCreationForm
    template_name = 'registration/admin_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('admin:complete_company_profile')


def create_company_after_signup_view(request,id):
    if request.method == "POST":
        form = CompanyForm(request.POST,request.FILES)
        user = User.objects.get(id=id)
        comp_admin = CompanyAdmin.objects.get(user=user)
        company_type = ""
        if comp_admin.is_suplier:
            company_type = "supplier"
            company_type_am = "አቅራቢ"
        elif comp_admin.is_manufacturer:
            company_type = "manufacturer"
            company_type_am = "አምራች"

        if form.is_valid():
            company_info = Company.objects.create(
                user=user,
                company_name=form.cleaned_data.get("company_name"),
                company_name_am=form.cleaned_data.get("company_name_am"),
                email=form.cleaned_data.get("email"),
                phone_number=form.cleaned_data.get("phone_number"),
                company_type=company_type,
                company_type_am = company_type_am,
                location=form.cleaned_data.get('location'),
                company_logo=form.cleaned_data.get("company_logo"),
                company_intro=form.cleaned_data.get("company_intro"),
                detail=form.cleaned_data.get("detail"),
                detail_am=form.cleaned_data.get("detail_am")
            )
            company_info.save()
            return redirect("admin:login")
        else:
            return render(request,"admin/pages/company_form.html",{'form':form,'comp_user':user})
    else:
        form = CompanyForm()
        comp_user = User.objects.get(id=id)
        context = {'form':form,'comp_user':comp_user}
        return render(request,"admin/pages/company_form.html",context)
          
        

# company related view
class CreateCompanyProfileView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = CompanyForm()
        context = {}
        if self.kwargs['option'] == 'view':
            if self.request.user.is_company_admin:
                company_detail = Company.objects.get(user=self.request.user)
                context={'company':company_detail}
            elif self.request.user.is_company_staff:
                comp_staff = CompanyStaff.objects.get(user=self.request.user)
                company_detail = Company.objects.get(id=comp_staff.company.id)
                context={'company':company_detail}
            return render(self.request,"admin/pages/company_detail.html",context)
        elif self.kwargs['option'] == 'edit':
            company_detail = Company.objects.get(id=self.kwargs['id'])
            context={'company':company_detail,'edit':'edit'}
            return render(self.request,"admin/pages/company_profile.html",context)
        elif self.kwargs['option'] == 'create':
            context = {'form':form}
            return render(self.request,"admin/pages/company_profile.html",context)
        elif self.kwargs['option'] == "create_now":
            comp_user = User.objects.get(id=self.kwargs['id'])
            context = {'form':form,'comp_user':comp_user}
            return render(self.request,"admin/pages/company_form.html",context)
            
        
    
    def post(self,*args,**kwargs):
        comp_admin = CompanyAdmin.objects.get(user=self.request.user)
        company_type = ""
        if comp_admin.is_suplier:
            company_type = "supplier"
            company_type_am = "አቅራቢ"
        elif comp_admin.is_manufacturer:
            company_type = "manufacturer"
            company_type_am = "አምራች"

        if self.kwargs['option'] == 'create':
            form = CompanyForm(self.request.POST,self.request.FILES)
            if form.is_valid():
                company_info = Company(
                    user=self.request.user,
                    company_name=form.cleaned_data.get("company_name"),
                    company_name_am=form.cleaned_data.get("company_name_am"),
                    email=form.cleaned_data.get("email"),
                    phone_number=form.cleaned_data.get("phone_number"),
                    company_type=company_type,
                    location=form.cleaned_data.get('location'),
                    company_logo=form.cleaned_data.get("company_logo"),
                    company_intro=form.cleaned_data.get("company_intro"),
                    detail=form.cleaned_data.get("detail"),
                    detail_am = form.cleaned_data.get("detail_am"),
                    )
                company_info.save()
                messages.success(self.request,"Company Profile Created")
                return redirect("admin:comp_profile",option="view",id=company_info.id)
        elif self.kwargs['option'] == 'edit':
            print(self.request.POST.get("company_name"))
            company_info = Company.objects.get(id=self.request.POST['comp_id'])
            company_info.company_name=self.request.POST['company_name']
            company_info.company_name_am=self.request.POST['company_name_am']
            company_info.email=self.request.POST['email']
            company_info.phone_number=self.request.POST['phone_number']
            company_info.location=self.request.POST['location']
            if self.request.FILES.get('company_logo') == None:
                pass
            elif self.request.FILES.get('company_logo') != None:
                company_info.company_logo=self.request.FILES.get('company_logo')
            if self.request.FILES.get("company_intro") == None:
                pass
            elif self.request.FILES.get("company_intro") != None:
                company_info.company_intro=self.request.FILES.get("company_intro")
            company_info.detail=self.request.POST["detail"]
            company_info.detail_am=self.request.POST["detail_am"]
            company_info.save()
            messages.success(self.request,"Company Profile Created")
            return redirect("admin:comp_profile",option="view",id=company_info.id)

class CreateCompanyProfile(LoginRequiredMixin,View):
    def get(self, *args,**kwargs):
        form = CompanyForm()
        return render(self.request,"admin/pages/form_wizard.html",{"form":form})

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerCreationForm
    template_name = 'registration/customer_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.save()
        sendEmailVerification(self.request,user)
        return render(self.request,'email/confirm_registration_message.html',
            {'message':"Please Verify your email address to complete the registration\n"
            +"If you can\'t find the mail please check it in your spam folder!"})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        sendWelcomeEmail(request,user)
        return render(request,'email/confirm_registration_message.html',
        {'message':"Thank you for your email confirmation. Now you can login to your account.",'url':'login'})
    else:
        return render(request,'email/confirm_registration_message.html',
        {'message':"Activation link is invalid!"})


class UpdateAdminProfile(LoginRequiredMixin,View):

    def post(self,*args,**kwargs):
        user = User.objects.get(id=self.request.user.id)
        if self.request.POST['username'] != None:
            user.username = self.request.POST['username']
        if self.request.POST['first_name'] != None:
            user.first_name = self.request.POST['first_name']
        if self.request.POST['last_name'] != None:
            user.last_name = self.request.POST['last_name']
        if self.request.POST['phone_number'] != None:
            user.phone_number = self.request.POST['phone_number']
        if self.request.FILES.get('profile_image') != None:
            user.profile_image = self.request.FILES.get('profile_image')
        
        user.save()
        messages.success(self.request,"You Have Successfully Updated Your Profile")
        return redirect("admin:user_detail",option="my_profile",id=self.request.user.id)
        

class UserListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {}
        if self.request.user.is_superuser:
            users = User.objects.all().exclude(id=self.request.user.id)
            context = {'users': users}
        elif self.request.user.is_company_admin:
            try:
                company = Company.objects.get(user=self.request.user)
                company_users = CompanyStaff.objects.filter(company=company)
                context = {'users': company_users}
            except ObjectDoesNotExist:
                messages.warning(self.request,"Please Complete Your Company Profile First and Create Your Company Staff\n")
                return redirect('admin:comp_profile',option="create",id=self.request.user.id)
        elif self.request.user.is_company_staff:
            try:
                staff_obj = CompanyStaff.objects.get(user=self.request.user)
                company_users=CompanyStaff.objects.filter(company=staff_obj.company).exclude(user=self.request.user)
                context = {'users':company_users}
            except ObjectDoesNotExist:
                messages.warning(self.request,"You Are Not Authrized To View The Users")
                return redirect('admin:index')
        return render(self.request, "admin/pages/users_list.html", context)


class UserDetailView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {}
        if self.kwargs['option'] == 'my_profile':
            user_company = None
            user_profile = None
            user_type = ""
            if self.request.user.is_superuser:
                user_profile = self.request.user
                user_type = "super_admin"
            elif self.request.user.is_company_admin:
                user_profile = CompanyAdmin.objects.get(user=self.request.user)
            elif self.request.user.is_company_staff:
                user_profile = CompanyStaff.objects.get(user=self.request.user)
            
            try:
                user_company = Company.objects.get(user=self.request.user)
            except ObjectDoesNotExist:
                pass

            context = {
                'user_company':user_company,'users':user_profile,'user_type':user_type
            }
        elif self.kwargs['option'] == 'profile_dtl':
            user = User.objects.get(id=self.kwargs['id'])
            user_profile = None
            if user.is_superuser:
                user_profile = user
            elif user.is_company_admin:
                user_profile = CompanyAdmin.objects.get(user=user)
            elif user.is_company_staff:
                user_profile = CompanyStaff.objects.get(user=user)
            elif user.is_customer:
                user_profile = Customer.objects.get(user=user)
            context = {'users': user_profile,}
        return render(self.request, "admin/pages/user_profile.html", context)


class CreateUserView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = ""
        context = {}

        if self.request.user.is_superuser:
            form = AdminCreateUserForm()
            context = {'form':form}
        elif self.request.user.is_company_admin:
            form = CompanyUserCreationForm()
            context = {'form':form}
        return render(self.request, "admin/pages/user_form.html", context)

    def post(self, *args, **kwargs):
        form = ""
        if self.request.user.is_superuser:
            form = AdminCreateUserForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(self.request,"You Created a User Successfully!")
                return redirect("admin:users_list")
            else:
                return render(self.request, "admin/pages/user_form.html", {"form": form})
        elif self.request.user.is_company_admin:
            form = CompanyUserCreationForm(self.request.POST)
            if form.is_valid():
                user = form.save()
                company = Company.objects.get(user=self.request.user)
                comp_staff = CompanyStaff.objects.create(user=user,company=company)
                comp_staff.save()
                messages.success(self.request,"You Created a User Successfully!")
                return redirect("admin:users_list")
            else:
                return render(self.request, "admin/pages/user_form.html", {"form": form})
            
        

class GroupView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        obj = Group.objects.all()
        permissions = Permission.objects.all()
        return render(self.request,"admin/pages/group_form.html",{'permisions':permissions,'objs':obj})

    def post(self,*args,**kwargs):
        permission_list = []
        for permision_id in self.request.POST.getlist('sel_perm_list[]'):
            permission_list.append(Permission.objects.get(id=permision_id))
        group,created = Group.objects.get_or_create(name = self.request.POST.get('group_name'))
        group.permissions.set(permission_list)
        group.save()
        return HttpResponse({"message":"Role Group Created SuccessFully","group":group})





class RolesView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        roles = Permission.objects.all()
        # role_user = User.objects.get(id=self.kwargs['userid'])
        # asigned_role = AssignedRoles.objects.filter(user=role_user)
        context = {'roles':roles}
        return render(self.request,"admin/pages/roles_list.html",context)
    
    def post(self,*args,**kwargs):
        new_roles = self.request.POST.getlist('new_roles[]')
        # role_user = User.objects.get(id=self.kwargs['userid'])
        # print(role_user)
        # if len(new_roles) > 0:
        #     print("its above zero")
        #     rem_roles = AssignedRoles.objects.filter(user=role_user).delete()
        #     print(rem_roles)
        #     for role_id in new_roles:
        #         permision = Permission.objects.get(id=role_id)
        #         print(permision)
        #         new_asigned,created = AssignedRoles.objects.get_or_create(
        #             user=role_user,
        #             roles=permision
        #         )
        #         new_asigned.save()
        #         print(new_asigned)
        # else:
        #     print("not above zero")
        #     remove_role = AssignedRoles.objects.filter(user=role_user)
        #     remove_role.delete()
        #     print(remove_role)
        return HttpResponse("Role Assigned Successfully")


class UserLogView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        failed_logins = FailedLoginLog.objects.all()
        login_logs = LoginLog.objects.all()
        login_attempt = LoginAttempt.objects.all()
        deactivation = UserDeactivation.objects.all()
        context = {
        'failed_logins':failed_logins,'login_attempts':login_attempt,
        'login_logs':login_logs,'user_deactivated':deactivation
        }
        return render(self.request,"admin/pages/user_logs.html",context)

