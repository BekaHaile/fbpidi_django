from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission,Group



from useraudit.models import FailedLoginLog,LoginAttempt,LoginLog,UserDeactivation

from accounts.forms import (UserCreationForm, ProfileForm, AdminCreateUserForm,
                            CompanyUserCreationForm,GroupCreationForm)
from accounts.models import User, ProfileImage,AssignedRoles,Company

class CustomerAdminSignUpView(View):

    def get(self, *args, **kwargs):
        form = UserCreationForm()
        return render(self.request, "registration/signup.html", {'form': form})

    def post(self, *args, **kwargs):
        form = UserCreationForm(self.request.POST)
        if form.is_valid():
            print(form.cleaned_data.get("phone_number"))
            if form.cleaned_data.get("usertype") == "supplier":
                user = User(
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    username=form.cleaned_data.get("username"),
                    email=form.cleaned_data.get("email"),
                    phone_number=form.cleaned_data.get("phone_number")
                )
                user.staff = True
                user.is_active = True
                user.is_suplier = True
                user.set_password(form.cleaned_data.get("password1"))
                user.save()
                return redirect("ccp_al",id=user.id)
            elif form.cleaned_data.get("usertype") == "manufacture":
                user = User(
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    username=form.cleaned_data.get("username"),
                    email=form.cleaned_data.get("email"),
                    phone_number=form.cleaned_data.get("phone_number")
                )
                user.staff = True
                user.is_active = True
                user.is_manufacturer = True
                user.set_password(form.cleaned_data.get("password1"))
                user.save()
                return redirect("ccp_al",id=user.id)
            elif form.cleaned_data.get("usertype") == "superuser":
                user = User(
                    first_name=form.cleaned_data.get("first_name"),
                    last_name=form.cleaned_data.get("last_name"),
                    username=form.cleaned_data.get("username"),
                    email=form.cleaned_data.get("email"),
                    phone_number=form.cleaned_data.get("phone_number")
                )
                user.staff = True
                user.is_active = True
                user.admin = True
                user.set_password(form.cleaned_data.get("password1"))
                user.save()
            # user = User(
            #     username=form.cleaned_data.get("username"),
            #     email=form.cleaned_data.get("email"),
            #     is_superuser=True,
            #     is_staff=True
            #     )
            # user.set_password(form.cleaned_data.get("password1"))
            # user.save()
            return redirect("admin:login")
        else:
            print(form.errors)
        return render(self.request, "registration/signup.html", {'form': form})


def profileImage(request):

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data.get("profile_image"))
            profile_img,created = ProfileImage.objects.get_or_create(user=request.user)
            profile_img.profile_image=form.cleaned_data.get("profile_image")
            profile_img.save()
            return redirect("user_detail",option="my_profile",id=request.user.id)
        else:
            print(form.errors)
            return redirect("user_detail",option="my_profile",id=request.user.id)
    return redirect("user_detail",option="my_profile",id=request.user.id)


class UserListView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.user.is_admin:
            users = User.objects.all().exclude(id=self.request.user.id)
            pimages = ProfileImage.objects.all().exclude(user=self.request.user)
            context = {'users': users, 'pimages': pimages}
        else:
            company = Company.objects.get(user=self.request.user)
            users = User.objects.filter(created_by_admin_id=self.request.user.id) 
            # pimages = ProfileImage.objects.all().exclude(user=self.request.user)
            context = {'users': users, 'pimages': 'pimages'}
        return render(self.request, "admin/pages/users_list.html", context)


class UserDetailView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {}
        if self.kwargs['option'] == 'my_profile':
            form = ProfileForm()
            users = User.objects.get(id=self.kwargs['id'])
            roles = AssignedRoles.objects.filter(user=users)
            pimage = None
            user_company = None
            try:
                pimage = ProfileImage.objects.get(user=self.request.user)
                user_company = Company.objects.filter(user=users)
            except ObjectDoesNotExist:
                # messages.warning(self.request, "User Does Not Exist")
                # return redirect("admin:index")
                pass
            context = {
                'form': form, 'users': users, 'pimage': pimage,'user_company':user_company,'roles':roles
            }
        elif self.kwargs['option'] == 'profile_dtl':
            users = User.objects.get(id=self.kwargs['id'])
            roles = AssignedRoles.objects.filter(user=users)
            pimage = None
            try:
                pimage = ProfileImage.objects.get(user=users)
            except ObjectDoesNotExist:
                # messages.warning(self.request, "User Does Not Exist")
                # return redirect("users_list")
                pass
            context = {
                'users': users, 'pimage': pimage,'roles':roles
            }
        return render(self.request, "admin/pages/user_profile.html", context)


class CreateUserView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = ""
        context = {}
        if self.kwargs['admin_type'] == 'super_admin':
            form = AdminCreateUserForm()
            context = {'form':form,'super_admin':'super_admin'}
        elif self.kwargs['admin_type'] == 'comp_admin':
            form = CompanyUserCreationForm()
            context = {'form':form,'comp_admin':'comp_admin'}

        return render(self.request, "admin/pages/user_form.html", context)

    def post(self, *args, **kwargs):
        admin_type = self.kwargs['admin_type']
        form = ""
        if admin_type == 'comp_admin':
            form = CompanyUserCreationForm(self.request.POST)
        elif admin_type == 'super_admin':
            form = AdminCreateUserForm(self.request.POST)
        
        if form.is_valid():
            
            user = User(
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                phone_number=form.cleaned_data.get("phone_number")
            )
            if admin_type == 'supper_admin':
                user_type = form.cleaned_data.get("user_roles")
                if user_type == "admin":
                    user.staff=True
                    user.admin = True
                elif user_type == "suplier":
                    user.staff = True
                    user.is_suplier=True
                elif user_type == "manufacturer":
                    user.staff = True
                    user.is_manufacturer=True
                elif user_type == "customer":
                    pass
            elif admin_type == 'comp_admin':
                group_name = Group.objects.get(id=form.cleaned_data.get('group_name').id)
                user.created_by_admin_id = self.request.user.id
                if self.request.user.is_suplier:
                    user.is_suplier = True
                elif self.request.user.is_manufacturer:
                    user.is_manufacturer=True
                user.group_name = group_name
                user.staff = True
            else:
                pass
            user.is_active=True
            user.set_password(form.cleaned_data.get("password1"))
            user.save()
            messages.success(self.request,"You Created a User Successfully!")
            return redirect("users_list")
        else:
            return render(self.request, "admin/pages/user_form.html", {"form": form})

class GroupView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = GroupCreationForm()
        obj = Group.objects.all()
        return render(self.request,"admin/pages/group_form.html",{'form':form,'objs':obj})

    def post(self,*args,**kwargs):
        form = GroupCreationForm(self.request.POST)
        if form.is_valid():
            group,created = Group.objects.get_or_create(name = form.cleaned_data.get("name"))
            group.permissions.set(form.cleaned_data.get('permissions'))
            group.save()
            messages.success(self.request,"Group Created Success Fully")
            return redirect("group_view")
        else:
            return render(self.request,"admin/pages/group_form.html",{'form':form})


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

