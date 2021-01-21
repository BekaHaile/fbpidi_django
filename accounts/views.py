# django imports
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission,Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
#from admin_site.perm_mixins import

# third party app imports
from useraudit.models import FailedLoginLog,LoginAttempt,LoginLog,UserDeactivation

from accounts.forms import (CompanyAdminCreationForm,CustomerCreationForm,CompanyUserCreationForm,
                            AdminCreateUserForm,GroupCreationForm,CompanyForm)
from accounts.models import User,Company,CompanyAdmin,Customer
from company.models import CompanyStaff
from accounts.email_messages import sendEmailVerification,sendWelcomeEmail
 
class CompanyAdminSignUpView(CreateView):
        user = form.save()
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request,"You Already have Account,Please logout and create an account")
            return redirect("admin:index")
        else:
            form = CompanyAdminCreationForm()
            return render(self.request,'registration/admin_signup.html',{"form":form})
     
    def post(self, *args,**kwargs):
        form = CompanyAdminCreationForm(self.request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:complete_company_profile')
        else:
            return render(self.request,'registration/admin_signup.html',{'form':form})

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

class CompleteLoginView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        
        user = User.objects.get(id=self.request.user.id)
        if user.is_staff:
            return redirect("admin:index")
        else:
            if user.is_customer == False:
                user.is_customer = True
                user.save()
                customer = Customer(
                    user=user
                )
                customer.save()
            return redirect("index")


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
                return redirect('admin:create_company_profile')
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

class GroupList(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        groups = Group.objects.all()
        return render(self.request,"admin/pages/group_list.html",{'groups':groups})      
        

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
        return JsonResponse({"message":"Role Group Created SuccessFully"})





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

