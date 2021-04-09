from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages



def company_created():
    def decorator(view_func):
        def wrap(request,*args,**kwargs):
            if request.user.is_company_admin:
                if request.user.get_company() == None:
                    return redirect("admin:create_my_company")
                else:
                    return view_func(request,*args,**kwargs) 
            elif request.user.is_superuser:
                if request.user.get_company() == None:
                    messages.warning(self.request,"Please Create Your Inistitute Profile")
                    return redirect("admin:create_fbpidi_company")
                else:
                    return view_func(request,*args,**kwargs) 
            else:
                return view_func(request,*args,**kwargs) 
        return wrap
    return decorator


def check_active_company():
    def decorator(view_func):
        def wrapper(request,*args,**kwargs):
            if request.user.is_company_admin:
                if request.user.get_company() != None:
                    if request.user.get_company().is_active == False:
                        return
                    else:
                        return view_func(request,*args,**kwargs)
                else:
                    return redirect("admin:create_my_company")
            else:
                return redirect("admin:create_my_company")
        return wrapper
    return decorator

