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
from admin_site.views import (AdminIndex,DeleteView, Polls, CreatePoll, AddChoice,
                        EditPoll,EditChoice, DeletePoll, DetailPoll, DeleteChoice)


from collaborations.views import ( 
                        AdminNewsList, CreateNews, EditNews,  NewsDetail,

                        TenderList, CreateTender, TenderDetail, EditTender,  DeleteTender, ManageBankAccount

                        )
from collaborations.Views.blog import(
                        CreatBlog,AdminBlogList,BlogView, )

from product.views import (CreateCategories,CategoryDetail, AdminProductListView,CreateProductView,
                            ProductDetailView,AddProductImage,CreatePrice,CategoryView
                            )

from collaborations.Views.announcement import (AnnouncementDetail,ListAnnouncement,)  
                            
from company.views import (
    CompaniesDetailView,CompaniesView,CreateCompanyProfile,CreateCompanyEvent,EditCompanyEvent,
    CreateCompanyProfileAfterSignUp,ViewCompanyProfile,CreateCompanySolution,
    CreateFbpidiCompanyProfile,ViewFbpidiCompany, CreateCompanyBankAccount, EditCompanyBankAccount, DeleteCompanyBankAccount
)
from collaborations.views import PollIndex
from accounts.api.api_views import CompanyAdminSignUpView, CustomerSignUpView
from rest_framework.authtoken.views import obtain_auth_token
# from collaborations.api.api_views import PollApiView, ChoicesView, ChoicesApiView, PollsApi

urlpatterns = [ 
     
    path("companyadminsignup/", CompanyAdminSignUpView.as_view(), name = "api_companyadmin_signup" ),
    path("login/", obtain_auth_token, name = "api_login"),
    # path("polls/", PollApiView.as_view(), name = "api_admin_polls"),
    # path("polls/<int:pk>/", PollsApi.as_view(), name = "polls_api"),
    # path("choices/<id>/", ChoicesApiView.as_view(), name = "api_admin_choices" ),
    # # path("choices/", ChoicesApiView.as_view(), name = "api_admin_choices" ),

#             
     

]


#  my_urls = [ 
#             path('anounce-Detail/<model_name>/<id>',AnnouncementDetail.as_view(),name="anounce_Detail"),
#             path('anounce-List',ListAnnouncementAdmin.as_view(),name="anounce_list"),
#             path('anounce-Create',CreatAnnouncement.as_view(),name="anounce_Create"),
#             #path('jobCategoty-detail/<model_name>/<id>',JobCategoryDetail.as_view(),name='Category_form'),
           
#             path('', wrap(AdminIndex.as_view()),name="admin_home"),
#             path('download/<name>/<id>',Download.as_view(),name="Download"),
#             path('close/<id>/<closed>',CloseVacancy.as_view(),name="close"),
#             path('applicant-info/<id>',Applicantinfo.as_view(),name="Applicant_info"),
#             path('applicant-list',ApplicantList.as_view(),name="Applicant_list"),
            
#             path('jobCategoty-form',JobcategoryFormView.as_view(),name="JobCategoty_form"),
#             path('jobCategoty-list',JobCategoryList.as_view(),name="admin_jobcategoty"),
#             path('jobCategoty-detail/<model_name>/<id>',JobCategoryDetail.as_view(),name='Category_form'),
           
#             path("Vacancy-form/",CreateVacancy.as_view(),name="Job_form"),
#             path("Vacancy-list/",AdminVacancyList.as_view(),name="Job_list"),
#             path("Vacancy-list-super/",SuperAdminVacancyList.as_view(),name="super_Job_list"),
#             path("Vacancy-detail/<model_name>/<id>",VacancyDetail.as_view(),name="job_detail"),
           
#             path("faqs-detail/<model_name>/<id>",FaqsView.as_view(),name="faqs_detail"),
#             path("faq-form/",CreateFaqs.as_view(),name="admin_Faqsform"),
#             path("faq-list/",FaqsList.as_view(),name="admin_Faqs"),
            
#             path("blog-list/",AdminBlogList.as_view(),name="admin_Blogs"),
#             path("blog-detail/<model_name>/<id>/",BlogView.as_view(),name="blog_detail"),
#             path("blog-create/",CreatBlog.as_view(),name="create_blog"),
            
#             path("signup/",CompanyAdminSignUpView.as_view(),name="signup"), done
#             path("create_user/",wrap(CreateUserView.as_view()),name="create_user"),
#             path("users_list/",wrap(UserListView.as_view()),name="users_list"),
#             path("roles_list/",wrap(RolesView.as_view()),name="roles_list"),
#             path("user_detail/<option>/<id>/",wrap(UserDetailView.as_view()),name="user_detail"),
#             path("update_profile/",wrap(UpdateAdminProfile.as_view()),name="add_profile"),
#             path("user_audit/",wrap(UserLogView.as_view()),name="useraudit"),
#             path("manage_group/",wrap(GroupView.as_view()),name="group_view"),

#             path("categories/<option>/",wrap(CategoryView.as_view()),name="p_categories"),
#             path("create_category/<option>",wrap(CreateCategories.as_view()),name="create_category"),
#             path("category_edit/<option>/<cat_id>/",wrap(CategoryDetail.as_view()),name="edit_category"),
#             path("delete/<model_name>/<id>/",wrap(DeleteView.as_view()),name="delete"),
#             path("products_list/<user_type>/",wrap(AdminProductListView.as_view()),name="admin_products"),
#             path("create_product/",wrap(CreateProductView.as_view()),name="create_product"),
#             path("product_detail/<option>/<id>/",wrap(ProductDetailView.as_view()),name="product_detail"),
#             path("add_more_images/",wrap(AddProductImage.as_view()),name="add_product_image"),
#             path("create_price/",wrap(CreatePrice.as_view()),name="create_price"),
            
#             # paths for polls, 
#             path("polls/", wrap(Polls.as_view()), name = "admin_polls"),
#             path("create_poll/", wrap(CreatePoll.as_view()), name = "create_poll"),
#             path("edit_poll/<id>/", wrap(EditPoll.as_view()), name = "edit_poll"),
#             path("add_choice/<id>/", wrap(AddChoice.as_view()), name = "add_choice"),
#             path("edit_choice/", wrap(EditChoice.as_view()), name = "edit_choice"), #choice id is found from edit_poll.html option tag
#             path("delete_poll/<id>/", wrap(DeletePoll.as_view()), name = "delete_poll"),
#             path("delete_choice/<id>/", wrap(DeleteChoice.as_view()), name = "delete_choice"),
#             path("detail_poll/<id>/", wrap(DetailPoll.as_view()), name = "detail_poll"),

#             # paths for tenders
#             path("tenders/", TenderList.as_view(), name = "tenders"),
#             path("create_tender/", CreateTender.as_view(), name = "create_tender"),
#             path("tender_detail/<id>/", wrap(TenderDetail.as_view()), name = "tender_detail"),
#             path("edit_tender/<id>/", EditTender.as_view(), name = "edit_tender"),
            
#             path("delete_tender/<id>/", DeleteTender.as_view(), name = "delete_tender"),
#             path("manage_bank_account/<option>/<id>/",ManageBankAccount.as_view(), name = "manage_bank_account"),
            

#             # paths for news and events
#             path('news_list/', AdminNewsList.as_view(), name = "news_list"),
#             path('create_news/', CreateNews.as_view(), name = "create_news"),
            
#             path('edit_news/<id>/', EditNews.as_view(), name = "edit_news"),
#             path('news_detail/<id>/', NewsDetail.as_view(), name = "news_detail"),
            
 


