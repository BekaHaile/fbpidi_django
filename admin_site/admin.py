from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path,include
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from accounts.forms import UserCreationForm 
# views from accounts app
from accounts.views import (CompanyAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,UpdateAdminProfile,CreateUserView,GroupView)
# views from admin_site app
from admin_site.views import (AdminIndex,DeleteView, Polls, CreatePoll, AddChoice,
                        EditPoll,EditChoice, DeletePoll, DetailPoll, DeleteChoice)

from collaborations.views import (CreatBlog,AdminBlogList,BlogView, CreateFaqs,FaqsView,FaqsList,
                        CreateVacancy,AdminVacancyList,VacancyDetail,JobcategoryFormView,JobCategoryList,
                        JobCategoryDetail,ApplicantList,Applicantinfo,CloseVacancy,Download,
                        SuperAdminVacancyList
                        )
from product.views import (CreateCategories,CategoryDetail, AdminProductListView,CreateProductView,
                            ProductDetailView,AddProductImage,CreatePrice,CategoryView
                            )
                            
from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,CreateCompanyEvent,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile,CreateCompanySolution,
    CreateFbpidiCompanyProfile,ViewFbpidiCompany
)



from collaborations.views import TenderList, CreateTender, TenderDetail, EditTender, AddTenderBankAccount, DeleteTender

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = [ 
            path('', wrap(AdminIndex.as_view()),name="admin_home"),
            path('download/<name>/<id>',Download.as_view(),name="Download"),
            path('close/<id>/<closed>',CloseVacancy.as_view(),name="close"),
            path('applicant-info/<id>',Applicantinfo.as_view(),name="Applicant_info"),
            path('applicant-list',ApplicantList.as_view(),name="Applicant_list"),
            
            path('jobCategoty-form',JobcategoryFormView.as_view(),name="JobCategoty_form"),
            path('jobCategoty-list',JobCategoryList.as_view(),name="admin_jobcategoty"),
            path('jobCategoty-detail/<model_name>/<id>',JobCategoryDetail.as_view(),name='Category_form'),
           
            path("Vacancy-form/",CreateVacancy.as_view(),name="Job_form"),
            path("Vacancy-list/",AdminVacancyList.as_view(),name="Job_list"),
            path("Vacancy-list-super/",SuperAdminVacancyList.as_view(),name="super_Job_list"),
            path("Vacancy-detail/<model_name>/<id>",VacancyDetail.as_view(),name="job_detail"),
           
            path("faqs-detail/<model_name>/<id>",FaqsView.as_view(),name="faqs_detail"),
            path("faq-form/",CreateFaqs.as_view(),name="admin_Faqsform"),
            path("faq-list/",FaqsList.as_view(),name="admin_Faqs"),
            
            path("blog-list/",AdminBlogList.as_view(),name="admin_Blogs"),
            path("blog-detail/<model_name>/<id>/",BlogView.as_view(),name="blog_detail"),
            path("blog-create/",CreatBlog.as_view(),name="create_blog"),
            
            path("signup/",CompanyAdminSignUpView.as_view(),name="signup"),
            path("create_user/",wrap(CreateUserView.as_view()),name="create_user"),
            path("users_list/",wrap(UserListView.as_view()),name="users_list"),
            path("roles_list/",wrap(RolesView.as_view()),name="roles_list"),
            path("user_detail/<option>/<id>/",wrap(UserDetailView.as_view()),name="user_detail"),
            path("update_profile/",wrap(UpdateAdminProfile.as_view()),name="add_profile"),
            path("user_audit/",wrap(UserLogView.as_view()),name="useraudit"),
            path("manage_group/",wrap(GroupView.as_view()),name="group_view"),

            path("categories/<option>/",wrap(CategoryView.as_view()),name="p_categories"),
            path("create_category/<option>",wrap(CreateCategories.as_view()),name="create_category"),
            path("category_edit/<option>/<cat_id>/",wrap(CategoryDetail.as_view()),name="edit_category"),
            path("delete/<model_name>/<id>/",wrap(DeleteView.as_view()),name="delete"),
            path("products_list/<user_type>/",wrap(AdminProductListView.as_view()),name="admin_products"),
            path("create_product/",wrap(CreateProductView.as_view()),name="create_product"),
            path("product_detail/<option>/<id>/",wrap(ProductDetailView.as_view()),name="product_detail"),
            path("add_more_images/",wrap(AddProductImage.as_view()),name="add_product_image"),
            path("create_price/",wrap(CreatePrice.as_view()),name="create_price"),
        
            # paths for polls, 
            path("polls/", wrap(Polls.as_view()), name = "admin_polls"),
            path("create_poll/", wrap(CreatePoll.as_view()), name = "create_poll"),
            path("edit_poll/<id>/", wrap(EditPoll.as_view()), name = "edit_poll"),
            path("add_choice/<id>/", wrap(AddChoice.as_view()), name = "add_choice"),
            path("edit_choice/", wrap(EditChoice.as_view()), name = "edit_choice"), #choice id is found from edit_poll.html option tag
            path("delete_poll/<id>/", wrap(DeletePoll.as_view()), name = "delete_poll"),
            path("delete_choice/<id>/", wrap(DeleteChoice.as_view()), name = "delete_choice"),
            path("detail_poll/<id>/", wrap(DetailPoll.as_view()), name = "detail_poll"),

            # paths for tenders
            path("tenders/", TenderList.as_view(), name = "tenders"),
            path("create_tender/", CreateTender.as_view(), name = "create_tender"),
            path("tender_detail/<id>/", wrap(DetailPoll.as_view()), name = "tender_detail"),
            path("edit_tender/<id>/", EditTender.as_view(), name = "edit_tender"),
            path("delete_tender/<id>/", DeleteTender.as_view(), name = "delete_tender"),
            path("add_tenderbankaccount/<id>/",wrap(DeletePoll.as_view()), name = "add_tenderbankaccount"),
            

            # path("",include("company.urls")),
            

        
            # path("",wrap(include("company.urls"))),
            path("create_company_profile/",wrap(CreateCompanyProfile.as_view()),name="create_company_profile"),
            path("company_list/<option>/",wrap(CompaniesView.as_view()),name="companies"),
            path("company_detail/<id>/",wrap(CompaniesDetailView.as_view()),name="company_detail"),
            path("create_company_profile_al/",wrap(CreateCompanyProfileAfterSignUp.as_view()) ,name='complete_company_profile'),
            path("view_company_profile/",wrap(ViewCompanyProfile.as_view()) ,name='view_company_profile'),
            path("edit_company_profile/<id>/",wrap(ViewCompanyProfile.as_view()),name="edit_company_profile"),
            path("create_company_solution/<company_id>",wrap(CreateCompanySolution.as_view()),name="create_company_solution"),
            path("create_company_event/<company_id>",wrap(CreateCompanyEvent.as_view()),name="create_company_event"),
            path("create_fbpidi_company/",wrap(CreateFbpidiCompanyProfile.as_view()),name="create_fbpidi_company"),
            path("view_fbpidi_company/",wrap(ViewFbpidiCompany.as_view()),name="view_fbpidi_company"),
            path("edit_fbpidi_profile/<id>/",wrap(ViewFbpidiCompany.as_view()),name="edit_fbpidi_profile"),
        ]
        return my_urls + urls


admin_site = CustomAdminSite(name='myadmin')