from django.shortcuts import render,redirect,get_object_or_404


def error_404(request):
    return render(request,"admin/error/error_404.html")

def error_500(request):
    return render(request,"admin/error/error_500.html")

def error_403(request):
    return render(request,"admin/error/error_404.html")

def company_not_active(request):
    return render(request,"admin/error/error_inactive.html")