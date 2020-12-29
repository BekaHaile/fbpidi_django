from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages


from django.core.exceptions import ObjectDoesNotExist

# 
from core import models
from core.forms import SubCategoryForm,ProductCreationForm
from accounts.models import User,Company
from accounts.forms import CompanyForm




class IndexView(View):
    def get(self,*args,**kwargs):
        products = models.Product.objects.all()
        category = models.Category.objects.all()
        sub_category = models.SubCategory.objects.all()
        company = Company.objects.all()
        context = {'products':products,'category':category,'sub_category':sub_category,'companies':company}
        return render(self.request,"frontpages/index.html",context)