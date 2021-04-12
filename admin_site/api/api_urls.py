from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path,include
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# views from accounts app
from accounts.views import (CompanyAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,UpdateAdminProfile,CreateUserView,GroupView)


# views from admin_site app
from admin_site.views import (AdminIndex,DeleteView, Polls, CreatePoll, AddChoice,EditPoll,EditChoice, DeletePoll, DetailPoll, DeleteChoice)


from collaborations.views import ( AdminNewsList, CreateNews, EditNews,  NewsDetail,TenderList, CreateTender, TenderDetail, EditTender,  DeleteTender)
from collaborations.Views.blog import(CreatBlog,AdminBlogList,BlogView, )

from product.views import (CreateCategories,CategoryDetail, AdminProductListView,CreateProductView,ProductDetailView,AddProductImage,CreatePrice,CategoryView)
from collaborations.Views.announcement import (AnnouncementDetail,ListAnnouncement,)  
                            
from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,CreateCompanyEvent,EditCompanyEvent,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile,CreateCompanySolution,
    CreateFbpidiCompanyProfile,ViewFbpidiCompany, CreateCompanyBankAccount, EditCompanyBankAccount, DeleteCompanyBankAccount
)

from accounts.api.api_views import CompanyAdminSignUpView, CustomerSignUpView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [  
    path("login/", obtain_auth_token, name = "api_login"),
]
