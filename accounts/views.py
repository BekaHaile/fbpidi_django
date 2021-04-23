# django imports
import json
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views.generic import (CreateView,View,UpdateView,ListView)
from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission,Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string,get_template
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

#from admin_site.perm_mixins import

# third party app imports
from useraudit.models import FailedLoginLog,LoginAttempt,LoginLog,UserDeactivation

from accounts.forms import (CompanyAdminCreationForm,CustomerCreationForm,CompanyUserCreationForm,
                            AdminCreateUserForm,GroupCreationForm,FrontLoginForm)
from accounts.models import UserProfile,Company,CompanyAdmin,Customer,Subscription
from company.models import CompanyStaff,Company
from accounts.email_messages import sendEmailVerification,sendWelcomeEmail
from admin_site.decorators import company_created,company_is_active

# 
# INDEX VIEW
decorators = [never_cache, company_created(),company_is_active()]
# Login view for the front end/customer UserProfile
class LoginView(auth_views.LoginView):
    form_class = FrontLoginForm
    template_name = 'registration/login.html'

# signup view for the admin user or company contact person
class CompanyAdminSignUpView(CreateView):
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
            user = form.save()
            user.save()
            sendEmailVerification(self.request,user)
            return render(self.request,'email/confirm_registration_message.html',
                {'message':"Please Verify your email address to complete the registration\n"
                +"If you can\'t find the mail please check it in your spam folder!"})
            # return redirect('admin:complete_company_profile')
        else:
            return render(self.request,'registration/admin_signup.html',{'form':form})

# view for customer sign up
class CustomerSignUpView(CreateView):
    model = UserProfile
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


# copmlete login view
class CompleteLoginView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        
        user = UserProfile.objects.get(id=self.request.user.id)
        if user.is_staff:
            if user.is_company_admin:
                try:
                    Company.objects.get(contact_person=user)
                    return redirect("admin:index")
                except Company.DoesNotExist:
                    messages.warning(self.request,'Please Complete Your Company Profile')
                    return redirect("admin:create_my_company")
            else:
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

# for activating a user account or email verification.
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserProfile._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        sendWelcomeEmail(request,user)
        if user.is_staff:
            return render(request,'email/confirm_registration_message.html',
            {'message':"Thank you for your email confirmation. Now you can login to your account.",'url':'admin:login'})
        elif user.is_staff is False:
            return render(request,'email/confirm_registration_message.html',
            {'message':"Thank you for your email confirmation. Now you can login to your account.",'url':'login'})
    else:
        return render(request,'email/confirm_registration_message.html',
        {'message':"Activation link is invalid!"})

# 
def api_activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserProfile._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        sendWelcomeEmail(request,user)
        return render(request,'email/confirm_registration_message.html',
            {'message':"Thank you for your email confirmation. Now you can login to your account using FBPIDI app."})
    else:
        return render(request,'email/confirm_registration_message.html',
            {'message':"Activation link is invalid!"})


@method_decorator(decorators,name='dispatch')
class MyProfileView(LoginRequiredMixin,UpdateView):
    model = UserProfile
    fields = ('first_name', 'last_name','username', 'email', 'phone_number','profile_image')
    template_name = "admin/accounts/user_profile.html"

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"Your Profile Updated Successfully")
        return redirect("admin:my_profile",pk=self.request.user.id)
    
    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:user_detail",pk=self.kwargs['pk'])


# to list all users in the admin page
@method_decorator(decorators,name='dispatch')
class UserListView(LoginRequiredMixin, ListView):
    model=UserProfile
    template_name = "admin/accounts/users_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all().exclude(id=self.request.user.id)
        elif self.request.user.is_company_admin:
            return UserProfile.objects.filter(created_by=self.request.user).exclude(id=self.request.user.id)


# to see a users detail profile
@method_decorator(decorators,name='dispatch')
class UserDetailView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name','username', 'email', 'phone_number','profile_image']
    template_name = "admin/accounts/user_detail.html"

    def form_valid(self,form):
        form.save()
        messages.success(self.request,"User Info Updated Successfully")
        return redirect("admin:user_detail",pk=self.kwargs['pk'])

    def form_invalid(self,form):
        messages.warning(self.request,form.errors)
        return redirect("admin:user_detail",pk=self.kwargs['pk'])

@method_decorator(decorators,name='dispatch')
class SuspendUser(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            user = UserProfile.objects.get(id=self.kwargs['pk'])
            if self.kwargs['option'] == "suspend":
                user.is_active = False
                user.save()
                messages.success(self.request,"User Suspended")
                return redirect("admin:users_list")
            elif self.kwargs['option'] == 'enable':
                user.is_active = True
                user.save()
                messages.success(self.request,"User Activated")
                return redirect("admin:users_list")
            
        except UserProfile.DoesNotExist:
            messages.success(self.request,"The User Does Not Exist")
            return redirect("admin:users_list")

@method_decorator(decorators,name='dispatch')
class CreateCompanyStaff(LoginRequiredMixin,CreateView):
    model=UserProfile
    form_class = CompanyUserCreationForm
    template_name = "admin/accounts/user_form.html"

    def form_valid(self,form):
        user = form.save()
        user.created_by = self.request.user
        user.save()
        company = Company.objects.get(contact_person=self.request.user)
        comp_staff = CompanyStaff.objects.create(user=user,company=company)
        comp_staff.save()
        messages.success(self.request,"You Created a User Successfully!")
        return redirect("admin:users_list")

@method_decorator(decorators,name='dispatch')
class CreateUserView(LoginRequiredMixin, CreateView):
    model=UserProfile
    form_class=AdminCreateUserForm
    template_name = "admin/accounts/user_form.html"

    def form_valid(self,form):
        user = form.save()
        user.created_by = self.request.user
        user.save()
        messages.success(self.request,"You Created a User Successfully!")
        return redirect("admin:users_list")

@method_decorator(decorators,name='dispatch')
class GroupList(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        groups = Group.objects.all()
        return render(self.request,"admin/pages/group_list.html",{'groups':groups})      
        
@method_decorator(decorators,name='dispatch')
class GroupView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        permissions = Permission.objects.all()
        return render(self.request,"admin/pages/group_form.html",{'permisions':permissions})

    def post(self,*args,**kwargs):
        permission_list = []
        for permision_id in self.request.POST.getlist('sel_perm_list[]'):
            permission_list.append(Permission.objects.get(id=permision_id))
        group,created = Group.objects.get_or_create(name = self.request.POST.get('group_name'))
        group.permissions.set(permission_list)
        group.save()
        return JsonResponse({"message":"Role Group Created SuccessFully"})

@method_decorator(decorators,name='dispatch')
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
        return render(self.request,"admin/accounts/user_logs.html",context)



def Subscribe(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            try:
                subscription = Subscription( email=data['email'])
                subscription.save()
                mail_subject = f"Subscription Email Verification Required .{data['email']}"
                message = get_template('email/acct_activate_email.html').render({
                    'user': "user bota",
                    'domain': "FBPIDI",
                    'uid': subscription.id,
                    'token': "some token",
                    'redirect_url':'activate_subscribtion'
                })
                email = EmailMessage( mail_subject, message, to=[ data['email'] ])
                email.content_subtype = "html"
                try:
                    email.send(fail_silently=False)
                except Exception as e:
                    subscription.delete()
                    print ("Exception sending email ",e)
                    return JsonResponse(data={'error':True, 'message':'Error Occured while sending email, check your email and connection and try again! '}, safe=False )

                return JsonResponse(data={'error':False, 'message':'Successfull Subscription! '}, safe=False )
                
            except Exception as e :
                subscription.delete()
                print ("Exception sending email ",e)
                return JsonResponse(data={'error':True, 'message':'Error Subscription! '}, safe=False )
        except Exception as e:
            return JsonResponse(data={'error':True, 'message':f'The exception is {str(e)}'},  safe=False )


def activate_subscription(request, uidb64, token):
    try:
        sid = urlsafe_base64_decode(uidb64).decode()
        subscription = Subscription.objects.get(pk=sid)
        subscription.activate = True
        subscription.save()

        # sendWelcomeEmail(request,user)
        return render(request,'email/confirm_registration_message.html',
            {'message':"Thank you for your subscribtion! we will keep you updated of the latest news and blogs through your email."})
    except Exception as e:
        return render(request,'email/confirm_registration_message.html',
            {'message':"Activation Failed!"})


