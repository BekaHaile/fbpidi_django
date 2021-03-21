from django.contrib import admin
from functools import update_wrapper
from django.template.response import TemplateResponse
from django.urls import path,include
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
# from accounts.forms import UserCreationForm 
# views from accounts app
from accounts.views import (CompanyAdminSignUpView,UserListView,
                            UserLogView,SuspendUser,
                            UserDetailView,MyProfileView,
                            CreateUserView,CreateCompanyStaff,
                            GroupView,GroupList)
# views from admin_site app
from admin_site.views.views import (AdminIndex,DeleteView,  Polls, CreatePoll, AddChoice,
                        EditPoll,EditChoice,  DetailPoll)

from admin_site.views.dropdowns import (AllSettingsPage,
                                       CreateCompanyDropdownsMaster,
                                        UpdateCompanyDropdownsMaster,
                                        CreateProjectDropdownsMaster,
                                        UpdateProjectDropdownsMaster)

from collaborations.views import (  CreateNews, EditNews, NewsDetail,AdminNewsList,AdminCompanyEventList,
                                    CreateCompanyEvent,EditCompanyEvent, TenderList, CreateTender, TenderDetail, 
                                    EditTender,  ManageBankAccount,CreateDocument, DocumentListing, EditDocument, 
                        )
from collaborations.Views.faq import(CreateFaqs,FaqsView,FaqsList,FaqPendingList,FaqApprovdList,
                                    FaqApprove,FaqsDetail)

from collaborations.Views.vacancy import(CreateVacancy,AdminVacancyList,VacancyDetail,CreateVacancyCategory,
                        JobCategoryDetail,ApplicantList,Applicantinfo,CloseVacancy,Download,
                        SuperAdminVacancyList,ApplicantListDetail,)
from collaborations.Views.projects import(

                        ListProjectAdmin,CreateProjectAdmin,ProjectDetailAdmin,
                        ProjectDetailView,
                        

                        )
from collaborations.Views.announcement import(
                        ListAnnouncementAdmin,CreatAnnouncementAdmin,
                        AnnouncementDetailAdmin,)

from collaborations.Views.blog import(
                        AdminBlogList,BlogView,AdminBlogComments,
                        CreatBlog,ListBlogCommentAdmin,BlogCommentDetailAdmin)

from collaborations.Views.research import(

                        ListResearchAdmin,CreateResearchAdmin,ResearchDetailAdmin,
                        ListPendingResearchAdmin,ResearchDetailView,ResearchApprove,
                        CreateResearchCategory,ResearchCategoryDetail,
                        

                        )
from collaborations.Views.forums import(ListForumQuestionAdmin,CreateForumQuestionAdmin,ForumQuestionDetail,
                                          ListForumCommentAdmin,ForumCommentsDetail,
                                          ListCommentReplayAdmin,CommentReplayDetail,
                                          ListForumCommentByIdAdmin,ListCommentReplayByIdAdmin )

from product.views import *
                            
from company.views import *

from accounts.forms import AdminLoginForm
from chat.views import AdminChatList
 
class CustomAdminSite(admin.AdminSite):
    login_form = AdminLoginForm
    def get_urls(self):
        urls = super().get_urls()
      
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        my_urls = [
            path('forum-list',wrap(ListForumQuestionAdmin.as_view()),name="forum_list"),
            path('forum-form',wrap(CreateForumQuestionAdmin.as_view()),name="forum_form"),
            path('forum-detail/<model_name>/<id>',wrap(ForumQuestionDetail.as_view()),name="forum_detail"),
            
            path('Comment_replays/<id>',wrap(ListCommentReplayByIdAdmin.as_view()),name="Comment_replays"),
            path('Forum_comment/<id>',wrap(ListForumCommentByIdAdmin.as_view()),name="Forum_Comments"),
            path('forum-comment-list',wrap(ListForumCommentAdmin.as_view()),name="forum_comment_list"),
            path('forum-comment-detail/<model_name>/<id>',wrap(ForumCommentsDetail.as_view()),name="forum_comment_detail"),

            path('comment-replay-list',wrap(ListCommentReplayAdmin.as_view()),name="comment_replay_list"),
            path('comment-replay-detail/<model_name>/<id>',wrap(CommentReplayDetail.as_view()),name="comment_replay_detail"),

            # #admin project 
            # path('project-form',wrap(CreateProjectAdmin.as_view()),name="project_form"),
            # path('project-list',wrap(ListProjectAdmin.as_view()),name="project_list"),
            # path('project-detail/<model_name>/<id>',wrap(ProjectDetailAdmin.as_view()),name="project_detail"),

            path('research-view/<id>',wrap(ResearchDetailView.as_view()),name='research_view'),
            path('research-approve/<id>',wrap(ResearchApprove.as_view()),name="research_approve"),
            path('pedning-research-list',wrap(ListPendingResearchAdmin.as_view()),name="pedning_research_list"),
            path('research-list',wrap(ListResearchAdmin.as_view()),name="research_list"),
            path('research-form',wrap(CreateResearchAdmin.as_view()),name="research_form"),
            path('research-detail/<model_name>/<id>',wrap(ResearchDetailAdmin.as_view()),name="research_detail"),

            path('research-categorys-detail/<pk>/',wrap(ResearchCategoryDetail.as_view()),name='researchprojectcategory_detail'),
            path('research-categorys-form/',wrap(CreateResearchCategory.as_view()),name='researchprojectcategory_form'), 
            
           
            path('', wrap(AdminIndex.as_view()),name="admin_home"),
            path('download/<name>/<id>',wrap(Download.as_view()),name="Download"),

            path('close/<id>/<closed>',wrap(CloseVacancy.as_view()),name="close"),
            path('applicant-info/<id>',wrap(Applicantinfo.as_view()),name="Applicant_info"),
            path('applicant-list',wrap(ApplicantList.as_view()),name="Applicant_list"),
            

            path('JobCategory-form',wrap(CreateVacancyCategory.as_view()),name="create_vacancy_category"),
            path('vacancy-Category-detail/<pk>/',wrap(JobCategoryDetail.as_view()),name='update_vacancy_category'),
           
            path("Vacancy-form/",wrap(CreateVacancy.as_view()),name="Job_form"),
            path("Vacancy-list/",wrap(AdminVacancyList.as_view()),name="Job_list"),
            path("Vacancy-list-super/",wrap(SuperAdminVacancyList.as_view()),name="super_Job_list"),
            path("Vacancy-applicant-info/<id>",wrap(ApplicantListDetail.as_view()),name="applicant_detail"),
            path("Vacancy-detail/<model_name>/<id>",wrap(VacancyDetail.as_view()),name="job_detail"),
           
            path("faq-detail/<model_name>/<id>",wrap(FaqsView.as_view()),name="faqs_detail"),
            path("faq-form/",wrap(CreateFaqs.as_view()),name="admin_Faqsform"),
            path("faq-list/",wrap(FaqsList.as_view()),name="admin_Faqs"),  
            path("faq-approved-list/",wrap(FaqApprovdList.as_view()),name="admin_approved_Faqs"),
            path("faq-pendding-list/",wrap(FaqPendingList.as_view()),name="admin_pendding_Faqs"),
            path("faq-approve/<id>",wrap(FaqApprove.as_view()),name="approve_Faqs"),
            path("faq-view/<model_name>/<id>",wrap(FaqsDetail.as_view()),name="view_Faqs"),

            
            path("blog-list/",wrap(AdminBlogList.as_view()),name="admin_Blogs"),
            path("blog-detail/<model_name>/<id>/",wrap(BlogView.as_view()),name="blog_detail"),
            path("blog-form/",wrap(CreatBlog.as_view()),name="create_blog"),
            path("blogComment-list/",wrap(ListBlogCommentAdmin.as_view()),name="blogComment_list"),
            path("blogComment-list/<id>",wrap(AdminBlogComments.as_view()),name="blogComment_list_id"), 
            path("blogComment-detail/<model_name>/<id>/",wrap(BlogCommentDetailAdmin.as_view()),name="blogComment_detail"),
            
            path("signup/",CompanyAdminSignUpView.as_view(),name="signup"), 
            path("create_user/",wrap(CreateUserView.as_view()),name="create_user"),
            path("create-my-staff/",wrap(CreateCompanyStaff.as_view()),name="create_my_staff"),
            path("users_list/",wrap(UserListView.as_view()),name="users_list"),
            path("suspend_user/<pk>/<option>/",wrap(SuspendUser.as_view()),name="suspend_user"),

            path("user_detail/<pk>/",wrap(UserDetailView.as_view()),name="user_detail"),
            path("update_my_profile/<pk>/",wrap(MyProfileView.as_view()),name="my_profile"),
            path("user_audit/",wrap(UserLogView.as_view()),name="useraudit"),
            path("group_list/",wrap(GroupList.as_view()),name="view_group"),
            path("manage_group/",wrap(GroupView.as_view()),name="create_group"),
            path("settings-page/",wrap(AllSettingsPage.as_view()),name='settings'),
            path('create-checklist/',wrap(CreateCompanyDropdownsMaster.as_view()),name='create_checklist'),
            path('update-checklist/<pk>/',wrap(UpdateCompanyDropdownsMaster.as_view()),name='update_checklist'),
            path('create-project-lookup/',wrap(CreateProjectDropdownsMaster.as_view()),name='create_plookup'),
            path('update-project-lookup/<pk>/',wrap(UpdateProjectDropdownsMaster.as_view()),name='update_plookup'),

            path("categories/",wrap(CategoryView.as_view()),name="categories"),
            path("create_category/",wrap(CreateCategories.as_view()),name="create_category"),
            path("category_edit/<pk>/",wrap(CategoryDetail.as_view()),name="edit_category"),
            path("sub_categories/",wrap(SubCategoryView.as_view()),name="sub_categories"),
            path("create_sub_category/",wrap(CreateSubCategories.as_view()),name="create_subcategory"),
            path("sub_category_edit/<pk>/",wrap(SubCategoryDetail.as_view()),name="edit_subcategory"),
            path("brands/",wrap(BrandView.as_view()),name="brands"),
            path("create_brand/",wrap(CreateBrand.as_view()),name="create_brand"),
            path("brand_edit/<pk>/",wrap(BrandDetail.as_view()),name="edit_brand"),
            path("delete/<model_name>/<id>/",wrap(DeleteView.as_view()),name="delete"),
            path("products_list/",wrap(AdminProductListView.as_view()),name="admin_products"),
            path("create_product/",wrap(CreateProductView.as_view()),name="create_product"),
            path("product_detail/<pk>/",wrap(ProductUpdateView.as_view()),name="product_detail"),
            path("add_more_images/<pk>/",wrap(AddProductImage.as_view()),name="add_product_image"),
            path("create_price/<pk>/",wrap(CreatePrice.as_view()),name="create_price"),
            path('create_dose/',wrap(CreateDose.as_view()),name="create_dose"),
            path('update_dose/<pk>/',wrap(UpdateDose.as_view()),name="update_dose"),
            path('update_dosage/<pk>/',wrap(UpdateDosageForm.as_view()),name="update_dosage"),
            path('create_dosage/',wrap(CreateDosageForm.as_view()),name="create_dosage"),
            path('production_capacity/<product>/',wrap(ListProductionCapacity.as_view()),name="production_capacity"),
            path('production_capacity_create/<product>/',wrap(CreateProductionCapacity.as_view()),name="create_production_capacity"),
            path('production_capacity_update/<pk>/',wrap(UpdateProductionCapacity.as_view()),name="update_production_capacity"),

            path('anual_input_need/<product>/',wrap(ListAnualInputNeed.as_view()),name="anual_input_need"),
            path('anual_input_need_create/<product>/',wrap(CreateAnualInputNeed.as_view()),name="create_anual_inp_need"),
            path('anual_input_need_update/<pk>/',wrap(UpdateAnualInputNeed.as_view()),name="update_anual_inp_need"),
            
            path('input_demand_spply/<product>/',wrap(ListInputDemandSupply.as_view()),name="demand_supply_list"),
            path('input_demand_supply_create/<product>/',wrap(CreateInputDemandSupply.as_view()),name="create_demand_supply"),
            path('input_demand_supply_update/<pk>/',wrap(UpdateInputDemandSupply.as_view()),name="update_demand_supply"),

            path('sales_performance/<product>/',wrap(ListSalesPerformance.as_view()),name="sales_performance"),
            path('sales_performance_create/<product>/',wrap(CreateSalesPerformance.as_view()),name="create_sales_performance"),
            path('sales_performance_update/<pk>/',wrap(UpdateSalesPerformance.as_view()),name="update_sales_performance"),
            
            path('packaging/<product>/',wrap(ListPackaging.as_view()),name="packaging"),
            path('create_packaging/<product>/',wrap(CreatePackaging.as_view()),name="create_packaging"),
            path('upadte_packaging/<pk>/',wrap(UpdatePackaging.as_view()),name="update_packaging"),


            # paths for polls, 
            path("polls/", wrap(Polls.as_view()), name = "admin_polls"),
            path("create_poll/", wrap(CreatePoll.as_view()), name = "create_poll"),
            path("edit_poll/<id>/", wrap(EditPoll.as_view()), name = "edit_poll"),
            path("add_choice/<id>/", wrap(AddChoice.as_view()), name = "add_choice"),
            path("edit_choice/", wrap(EditChoice.as_view()), name = "edit_choice"), #choice id is found from edit_poll.html option tag
            path("detail_poll/<pk>/", wrap(DetailPoll.as_view()), name = "detail_poll"),

            # paths for tenders
            path("tenders/", wrap(TenderList.as_view()), name = "tenders"),
            path("create_tender/", wrap(CreateTender.as_view()), name = "create_tender"),
            path("tender_detail/<pk>/", wrap(TenderDetail.as_view()), name = "tender_detail"),
            path("edit_tender/<id>/", wrap(EditTender.as_view()), name = "edit_tender"),
            path("manage_bank_account/<option>/<id>/",wrap(ManageBankAccount.as_view()), name = "manage_bank_account"),
            

            # paths for news and events
            path('news_list/', wrap(AdminNewsList.as_view()), name = "news_list"),
            path('create_news/', wrap(CreateNews.as_view()), name = "create_news"),
            path('edit_news/<id>/', wrap(EditNews.as_view()), name = "edit_news"),
            path('news_detail/<id>/', wrap(NewsDetail.as_view()), name = "news_detail"),

            path('admin_companyevent_list/', wrap(AdminCompanyEventList.as_view()), name = "admin_companyevent_list"),
            path("create_companyevent/",wrap(CreateCompanyEvent.as_view()),name="create_companyevent"),
            path("edit_companyevent/<pk>/",wrap(EditCompanyEvent.as_view()),name="edit_companyevent"),
            
            # path("",include("company.urls")),
            path("admin_chat_list/", wrap(AdminChatList.as_view()), name = "admin_chat_list"),

            # Company Paths
            # path("",wrap(include("company.urls"))),
            path("create_company_profile/",wrap(CreateCompanyProfile.as_view()),name="create_company_profile"),
            path("create_mycompany_profile/",wrap(CreateMyCompanyProfile.as_view()),name="create_my_company"),
            path("create_mycompany_detail/<pk>/",wrap(CreateMyCompanyDetail.as_view()),name="create_mycompany_detail"),
            path("create_company_detail_info/<pk>/",wrap(CreateCompanyDetail.as_view()),name="create_company_detail"),
            path("create_investment_capital/<company>/",wrap(CreateInvestmentCapital.as_view()),name="create_inv_capital"),
            path("update_investment_capital/<pk>/",wrap(UpdateInvestmentCapital.as_view()),name="update_inv_capital"),
            path("create_company_certificates/<company>/",wrap(CreateCertificates.as_view()),name="create_comp_certificate"),
            path("update_company_certificates/<pk>/",wrap(UpdateCertificate.as_view()),name="update_comp_certificate"),
            path("create_employees/<company>/",wrap(CreateEmployees.as_view()),name="create_employees"),
            path("update_employees/<pk>/",wrap(UpdateEmployees.as_view()),name="update_employees"),
            path("create_jobs_created/<company>/",wrap(CreateJobsCreatedYearly.as_view()),name="create_jobs_created"),
            path("update_jobs_created/<pk>/",wrap(UpdateJobsCreated.as_view()),name="update_jobs_created"),
            path("create_education_status/<company>/",wrap(CreateEducationStatus.as_view()),name="create_education_status"),
            path("update_education_status/<pk>/",wrap(UpdateEducationStatus.as_view()),name="update_education_status"),
            path("create_femalein_posn/<company>/",wrap(CreateFemaleinPosition.as_view()),name="create_female_posn"),
            path("update_femalein_posn/<pk>/",wrap(UpdateFemalesInPosn.as_view()),name="update_female_posn"),
            path("create_srcamnt_inputs/<company>/",wrap(CreateAnualSourceofInputs.as_view()),name="create_srcamnt_inputs"),
            path("update_srcamnt_inputs/<pk>/",wrap(UpdateSrcAmntInputs.as_view()),name="update_srcamnt_inputs"),
            path("create_market_destination/<company>/",wrap(CreateMarketDestination.as_view()),name="create_destination"),
            path("update_market_destination/<pk>/",wrap(UpdateMarketDestination.as_view()),name="update_destination"),
            path("create_market_target/<company>/",wrap(CreateMarketTarget.as_view()),name="create_target"),
            path("update_market_target/<pk>/",wrap(UpdateMarketTarget.as_view()),name="update_target"),
            path("create_power_consumption/<company>/",wrap(CreatePowerConsumption.as_view()),name="create_power_consumed"),
            path("update_power_consumption/<pk>/",wrap(UpdatePowerConsumption.as_view()),name="update_power_consumed"),
            path("create_company_address/<company>/",wrap(CreateCompanyAddress.as_view()),name="create_company_address"),
            path("update_company_address/<pk>/",wrap(UpdateCompanyAddress.as_view()),name="update_company_address"),
            path("update_company_info/<pk>",wrap(ViewMyCompanyProfile.as_view()),name="update_company_info"),
            path("check_company_year_data/<model>/<company>/<year>/",wrap(CheckYearField.as_view()),name="check_year_data"),

            path("company_list/",wrap(CompaniesView.as_view()),name="companies"),
            path("company_detail/<pk>/",wrap(CompaniesDetailView.as_view()),name="company_detail"),
            path("rate_company_status/<pk>/",wrap(RateCompany.as_view()),name="rate_company"),
            path("investment-project-list/",wrap(ListInvestmentProject.as_view()) ,name='project_list'),
            path("create-investment-project-company/",wrap(CreateMyInvestmentProject.as_view()),name="create_my_project"),
            path("create-investment-project-admin/",wrap(CreateInvestmentProject.as_view()),name="create_project"),
            path("complete-company-project-detail/<pk>/",wrap(CreateInvestmentProjectDetail.as_view()) ,name='create_project_detail'),
            path("complete-company-project-detail-admin/<pk>/",wrap(CreateInvestmentProjectDetail_Admin.as_view()) ,name='create_project_detail_admin'),
            path("update_investment_project/<pk>/",wrap(UpdateInvestmentProject.as_view()) ,name='update_project'),
            
            path("craete_land-usage/<project>/",wrap(CreateLandUsage.as_view()) ,name='create_land_use'),
            path("create_product_quantity/<project>/",wrap(CreateProductQty.as_view()) ,name='create_product_qty'),
            path("create_project_state/<project>/",wrap(CreateProjectState.as_view()) ,name='create_project_state'),

            path("update_land-usage/<pk>/",wrap(UpdateLandUsage.as_view()) ,name='update_land_use'),
            path("update_product_quantity/<pk>/",wrap(UpdateProductQty.as_view()) ,name='update_product_qty'),
            path("update_project_state/<pk>/",wrap(UpdateProjectState.as_view()) ,name='update_project_state'),

            path("create_fbpidi_company/",wrap(CreateFbpidiCompanyProfile.as_view()),name="create_fbpidi_company"),
            path("view_fbpidi_company/<pk>/",wrap(ViewFbpidiCompany.as_view()),name="view_fbpidi_company"),
            
            path("edit_fbpidi_profile/<id>/",wrap(ViewFbpidiCompany.as_view()),name="edit_fbpidi_profile"),

            ### Document
             path('create_document/', wrap(CreateDocument.as_view()), name='create_document'),
             path('edit_document/<id>/', wrap(EditDocument.as_view()), name='edit_document'),
             path('list_document_by_category/<option>/', wrap(DocumentListing.as_view()), name = "list_document_by_category"),


            path('forum-list',wrap(ListForumQuestionAdmin.as_view()),name="forum_list"),
            path('forum-form',wrap(CreateForumQuestionAdmin.as_view()),name="forum_form"),
            path('forum-detail/<model_name>/<id>',wrap(ForumQuestionDetail.as_view()),name="forum_detail"),

            path('forum-comment-list',wrap(ListForumCommentAdmin.as_view()),name="forum_comment_list"),
            path('forum-comment-detail/<model_name>/<id>',wrap(ForumCommentsDetail.as_view()),name="forum_comment_detail"),

            path('comment-replay-list',wrap(ListCommentReplayAdmin.as_view()),name="comment_replay_list"),
            path('comment-replay-detail/<model_name>/<id>',wrap(CommentReplayDetail.as_view()),name="comment_replay_detail"),

            # path('project-view/<id>',wrap(ProjectDetailView.as_view()),name='project_view'),
            # path('project-approve/<id>',wrap(ProjectApprove.as_view()),name="project_approve"),
            # path('pedning-project-list',wrap(ListPendingProjectAdmin.as_view()),name="pedning_project_list"),
            # path('project-list',wrap(ListProjectAdmin.as_view()),name="project_list"),
            # path('project-form',wrap(CreateProjectAdmin.as_view()),name="project_form"),
            # path('project-detail/<model_name>/<id>',wrap(ProjectDetailAdmin.as_view()),name="project_detail"),

            path('research-view/<id>',wrap(ResearchDetailView.as_view()),name='research_view'),
            path('research-approve/<id>',wrap(ResearchApprove.as_view()),name="research_approve"),
            path('pedning-research-list',wrap(ListPendingResearchAdmin.as_view()),name="pedning_research_list"),
            path('research-list',wrap(ListResearchAdmin.as_view()),name="research_list"),
            path('research-form',wrap(CreateResearchAdmin.as_view()),name="research_form"),
            path('research-detail/<model_name>/<id>',wrap(ResearchDetailAdmin.as_view()),name="research_detail"),

            # path('researchprojectcategorys-detail/<model_name>/<id>',wrap(ResearchCategoryDetail.as_view()),name='researchprojectcategory_detail'),
            # path('researchprojectcategorys-form',wrap(CreateResearchProjectCategoryAdmin.as_view()),name='researchprojectcategory_form'), 
            # path('researchprojectcategorys-list',wrap(ListResearchProjectCategoryAdmin.as_view()),name='research_project_category_list'),
            
            path('anounce-Detail/<id>/',wrap(AnnouncementDetailAdmin.as_view()),name="anounce_Detail"),
            path('anounce-List',wrap(ListAnnouncementAdmin.as_view()),name="anounce_list"),
            path('anounce-form',wrap(CreatAnnouncementAdmin.as_view()),name="anounce_Create"),
        ]
        return my_urls + urls


admin_site = CustomAdminSite(name='myadmin')