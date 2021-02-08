from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path,include
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from accounts.forms import UserCreationForm 
# views from accounts app
from accounts.views import (CompanyAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,UpdateAdminProfile,CreateUserView,GroupView,GroupList)
# views from admin_site app
from admin_site.views import (AdminIndex,DeleteView, Polls, CreatePoll, AddChoice,
                        EditPoll,EditChoice, DeletePoll, DetailPoll, DeleteChoice)

from collaborations.views import (CreatBlog,AdminBlogList,BlogView, CreateFaqs,FaqsView,FaqsList,
                        CreateVacancy,AdminVacancyList,VacancyDetail,JobcategoryFormView,JobCategoryList,
                        JobCategoryDetail,ApplicantList,Applicantinfo,CloseVacancy,Download,

                        SuperAdminVacancyList,ListAnnouncementAdmin,
                        AdminNewsList, CreateNews, EditNews, NewsDetail,
                        CreatAnnouncement,ListAnnouncement,AnnouncementDetail,TenderList, CreateTender, 
                        TenderDetail, EditTender,  DeleteTender, ManageBankAccount

                        )
from product.views import (CreateCategories,CategoryDetail, AdminProductListView,CreateProductView,
                            ProductDetailView,AddProductImage,CreatePrice,CategoryView
                            )
                            
from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,CreateCompanyEvent,EditCompanyEvent,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile,CreateCompanySolution,
    CreateFbpidiCompanyProfile,ViewFbpidiCompany, CreateCompanyBankAccount, EditCompanyBankAccount, DeleteCompanyBankAccount
)

 
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
      
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = [ 
            path('anounce-Detail/<model_name>/<id>',wrap(AnnouncementDetail.as_view()),name="anounce_Detail"),
            path('anounce-List', wrap(ListAnnouncementAdmin.as_view()),name="anounce_list"),
            path('anounce-Create',wrap(CreatAnnouncement.as_view()),name="anounce_Create"),
            #path('jobCategoty-detail/<model_name>/<id>',JobCategoryDetail.as_view(),name='Category_form'),
           
            path('', wrap(AdminIndex.as_view()),name="admin_home"),
            path('download/<name>/<id>',Download.as_view(),name="Download"),
            path('close/<id>/<closed>',wrap(CloseVacancy.as_view()),name="close"),
            path('applicant-info/<id>',wrap(Applicantinfo.as_view()),name="Applicant_info"),
            path('applicant-list',wrap(ApplicantList.as_view()),name="Applicant_list"),
            
            path('jobCategoty-form',wrap(JobcategoryFormView.as_view()),name="JobCategoty_form"),
            path('jobCategoty-list',wrap(JobCategoryList.as_view()),name="admin_jobcategoty"),
            path('jobCategoty-detail/<model_name>/<id>',wrap(JobCategoryDetail.as_view()),name='Category_form'),
           
            path("Vacancy-form/",wrap(CreateVacancy.as_view()),name="Job_form"),
            path("Vacancy-list/",wrap(AdminVacancyList.as_view()),name="Job_list"),
            path("Vacancy-list-super/",wrap(SuperAdminVacancyList.as_view()),name="super_Job_list"),
            path("Vacancy-detail/<model_name>/<id>",wrap(VacancyDetail.as_view()),name="job_detail"),
           
            path("faqs-detail/<model_name>/<id>",wrap(FaqsView.as_view()),name="faqs_detail"),
            path("faq-form/",wrap(CreateFaqs.as_view()),name="admin_Faqsform"),
            path("faq-list/",wrap(FaqsList.as_view()),name="admin_Faqs"),
            
            path("blog-list/",wrap(AdminBlogList.as_view()),name="admin_Blogs"),
            path("blog-detail/<model_name>/<id>/",wrap(BlogView.as_view()),name="blog_detail"),
            path("blog-create/",wrap(CreatBlog.as_view()),name="create_blog"),
            
            path("signup/",CompanyAdminSignUpView.as_view(),name="signup"),
            path("create_user/",wrap(CreateUserView.as_view()),name="create_user"),
            path("users_list/",wrap(UserListView.as_view()),name="users_list"),
            path("roles_list/",wrap(RolesView.as_view()),name="roles_list"),
            path("user_detail/<option>/<id>/",wrap(UserDetailView.as_view()),name="user_detail"),
            path("update_profile/",wrap(UpdateAdminProfile.as_view()),name="add_profile"),
            path("user_audit/",wrap(UserLogView.as_view()),name="useraudit"),
            path("group_list/",wrap(GroupList.as_view()),name="view_group"),
            path("manage_group/",wrap(GroupView.as_view()),name="create_group"),

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
            path("tenders/", wrap(TenderList.as_view()), name = "tenders"),
            path("create_tender/", wrap(CreateTender.as_view()), name = "create_tender"),
            path("tender_detail/<id>/", wrap(TenderDetail.as_view()), name = "tender_detail"),
            path("edit_tender/<id>/", wrap(EditTender.as_view()), name = "edit_tender"),
            
            path("delete_tender/<id>/", wrap(DeleteTender.as_view()), name = "delete_tender"),
            path("manage_bank_account/<option>/<id>/",wrap(ManageBankAccount.as_view()), name = "manage_bank_account"),
            

            # paths for news and events
            path('news_list/', wrap(AdminNewsList.as_view()), name = "news_list"),
            path('create_news/', wrap(CreateNews.as_view()), name = "create_news"),
            
            path('edit_news/<id>/', wrap(EditNews.as_view()), name = "edit_news"),
            path('news_detail/<id>/', wrap(NewsDetail.as_view()), name = "news_detail"),
            
            

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
            path("edit_company_event/<id>/",wrap(EditCompanyEvent.as_view()),name="edit_company_event"),
            path("create_fbpidi_company/",wrap(CreateFbpidiCompanyProfile.as_view()),name="create_fbpidi_company"),
            path("view_fbpidi_company/",wrap(ViewFbpidiCompany.as_view()),name="view_fbpidi_company"),
            path("edit_fbpidi_profile/<id>/",wrap(ViewFbpidiCompany.as_view()),name="edit_fbpidi_profile"),
            path("create_company_bank_account/<id>/", CreateCompanyBankAccount.as_view(), name = "create_company_bank_account"),
            path("edit_company_bank_account/<id>/", EditCompanyBankAccount.as_view(), name = "edit_company_bank_account"),
            path("delete_company_bank_account/<id>/", DeleteCompanyBankAccount.as_view(), name = "delete_company_bank_account"),

        ]
        return my_urls + urls


admin_site = CustomAdminSite(name='myadmin')