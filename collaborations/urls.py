from django.urls import path,include

from .views import (CustomerPollList, PollDetail, 
                    CustomerTenderList, CustomerTenderDetail,

                    ApplyForTender,ApplyForCompanyTender, CustomerNewsList, AjaxEventParticipation,AjaxApplyForTender,
                    CustomerNewsDetail,CustomerEventList, CustomerEventDetail, EventParticipation
                    )
from .Views.forums import (CreateForumQuestion , ListForumQuestions,
                        ForumQuestionsDetail,SearchForum,
                    CreateCommentReplay,EditCommentForum,EditForumQuestions,)
from .Views.blog import (CreateBlogComment,BlogList,BlogDetail,)
from .Views.vacancy import (VacancyMoreDetail, CreateApplication, VacancyList,
                    CategoryBasedSearch,)
from .Views.announcement import (AnnouncementDetail,ListAnnouncement,)  

from .Views.projects import (EditProject,ListProject,ProjectDetail,CreateProject
                            ,SearchProject,ProjectCategorySearch, ProjectDetailView)  
from .Views.faq import FaqList

from .Views.research import (EditResearch,ListResearch,ResearchDetail,CreateResearch,SearchResearch,
                    ResearchCategorySearch,CreateResearchAdmin)  
                    

urlpatterns = [ 
    path('project-view/<id>/',ProjectDetailView.as_view(),name='project_view'),
    
    path("project-list",ListProject.as_view(),name="project_list"),
    path('project-search',SearchProject.as_view(),name='project_search'),
    path("project-detail/<id>",ProjectDetail.as_view(),name="project_detail"),
    path("project-category/<id>",ProjectCategorySearch.as_view(),name="projectcategory_search"),

    path("research-list",ListResearch.as_view(),name="research_list"),
    path('research-form',CreateResearch.as_view(),name="research_form"),
    path("research-edit/<id>",EditResearch.as_view(),name="research_edit"),
    path('research-search',SearchResearch.as_view(),name='research_search'),
    path("research-detail/<id>",ResearchDetail.as_view(),name="research_detail"),
    path("research-category/<id>",ResearchCategorySearch.as_view(),name="researchcategory_search"),

    path("polls/", CustomerPollList.as_view(), name = "polls" ),
    path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),
    
    path("edit-comment/<id>/<forum>/<type>/",EditCommentForum.as_view(),name="edit_comment"),
    path("forum-edit/<id>",EditForumQuestions.as_view(),name="forum_edit"),
    path("forum-search",SearchForum.as_view(),name="forum_search"),
    path("forum-form",CreateForumQuestion.as_view(),name="forum_form"),
    path("forum-list",ListForumQuestions.as_view(),name="forum_list"),
    path("replay-comment/<id>/<forum>",CreateCommentReplay.as_view(),name="Replay_comment"),
    path("forum-detail/<id>/",ForumQuestionsDetail.as_view(),name="forum_detail"),

    path("announcement-list/",ListAnnouncement.as_view(),name="announcement_list"),
    path("announcement-detail/<id>/",AnnouncementDetail.as_view(),name="announcement_detail"),
    
    path("customer_tender_detail/<id>/", CustomerTenderDetail.as_view(), name = "customer_tender_detail"),
    path("tender_application/<id>/", ApplyForTender.as_view(), name= "tender_application"),
    path("tender-list/", CustomerTenderList.as_view(), name = "tender_list"),
    path("apply_company_tender/<id>/", ApplyForCompanyTender.as_view(), name = "apply_company_tender"),

    path("faq/",FaqList.as_view(),name="faq"),
    
    # path("search-tag/<name>",SearchBlogTag.as_view(),name="search_blogtag"),
    # path("search-tag_am/<name>",SearchBlogTag_Am.as_view(),name="search_blogtag_am"),
    path("blog-list/",BlogList.as_view(),name="customer_blog_list"),
    # path("blog-search/",SearchBlog.as_view(),name="blog_search"),
    path("blog-detail/<id>",BlogDetail.as_view(),name="blog_details"),
    path("blog-comment/<id>",CreateBlogComment.as_view(),name="Comment"),

    path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    path("vacancy-apply/<model_name>/<id>",CreateApplication.as_view(),name="applications"),
    path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    path("vacancy-detail/<id>",VacancyMoreDetail.as_view(),name="vacancy_detail"),

    ##News
    path("customer_news_list/", CustomerNewsList.as_view(), name = "customer_news_list"),
    path("customer_news_detail/<id>/", CustomerNewsDetail.as_view(), name = "customer_news_detail"),
    
    ##Events
    path("customer_event_list/", CustomerEventList.as_view(), name = "customer_event_list"),
    path("customer_event_detail/<id>/", CustomerEventDetail.as_view(), name = "customer_event_detail"),
    path("event_participation/<id>/", EventParticipation.as_view(), name="event_participation"),
    path("ajax_event_participation/<id>/", AjaxEventParticipation, name = "ajax_event_participation"),

  

    
        
]
