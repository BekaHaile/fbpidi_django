from django.urls import path,include
from collaborations.views import PollIndex
from collaborations.api.api_views import (PollListApiView, PollDetailApiView, NewsListApiView, NewsDetailApiView, 
        EventListApiView, EventDetailApiView, EventNotifyApiView, ApiAnnouncementList, ApiAnnouncementDetail,
        ApiBlogList, ApiBlogDetail, ApiCreateBlogComment, ApiTenderList, ApiTenderDetail, ApiVacancyList,
        ApiVacancyDetail, ApiVacancyApplication, ApiProject, ApiProjectDetail, ApiResearch, ApiResearchDetail,
        ApiForumQuestionList, ApiForumQuestionDetail, ApiCreateForumQuestion, ApiCommentAction, ApiCommentReplayAction,
        ApiCreateResearch, ApiResearchAction, ApiFaq)

urlpatterns = [ 
    
    path("polls/", PollListApiView.as_view(), name = "client_polls" ),
    path("poll_detail/<id>/", PollDetailApiView.as_view(), name = "client_poll_detail" ),
    path('news/', NewsListApiView.as_view(), name = "client_news"),
    path('news_detail/<id>/', NewsDetailApiView.as_view(), name = 'client_news_detail'),
    path('events/', EventListApiView.as_view(), name = 'client_events'),
    path('event_detail/<id>/', EventDetailApiView.as_view(), name = "client_event_detail"),
    path('event_notify/<id>/', EventNotifyApiView, name= 'event_notify'),

    ##Forum
    path("forum_list/", ApiForumQuestionList.as_view(), name = "api_forum_list"), 
    path("forum_detail/", ApiForumQuestionDetail.as_view(), name = 'api_forum_detail'),
    path("forum_action/", ApiCreateForumQuestion, name = "api_forum_create"),
    path('forum_comment_action/', ApiCommentAction, name = "api_comment_action"),
    path('forum_comment_replay_action/', ApiCommentReplayAction, name = "api_comment_replay_action"),
    # path("edit-comment/<id>/<forum>/<type>/",EditCommentForum.as_view(),name="edit_comment"),
    # path("forum-edit/<id>",EditForumQuestions.as_view(),name="forum_edit"),
    # path("forum-search",SearchForum.as_view(),name="forum_search"),
    # path("forum-form",CreateForumQuestion.as_view(),name="forum_form"),
    

    path("announcement-list/",ApiAnnouncementList.as_view(),name="api_announcement_list"),
    path("announcement-detail/",ApiAnnouncementDetail.as_view(),name="api_announcement_detail"),
    
    # path("apply/<model_name>/<id>",CreateApplication.as_view(),name="applications"),
    # path("forum-list",ListForumQuestions.as_view(),name="forum_list"),
    # path("Replay-comment/<id>/<forum>",CreateCommentReplay.as_view(),name="Replay_comment"),
    # path("forum-detail/<id>",ForumQuestionsDetail.as_view(),name="forum_detail"),
    
    path("tender_list/", ApiTenderList.as_view(), name = "api_tender_list"),
    path("tender_detail/", ApiTenderDetail.as_view(), name = "api_tender_detail"),
    
    path("faqs/",ApiFaq.as_view(),name="api_faq"),
    path("blog-list/",ApiBlogList.as_view(),name="api_blog_grid_right"),
    path("blog-details/",ApiBlogDetail.as_view(),name="api_blog_details"),
    path("blog-comment/",ApiCreateBlogComment,name="api_comment"),

    path("vacancy_list/",ApiVacancyList.as_view(),name="api_vacancy_list"),
    path("vacancy_apply/",ApiVacancyApplication.as_view(),name="api_vacanvy_apply"),
    # path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    path("vacancy_detail/",ApiVacancyDetail.as_view(),name="api_vacancy_detail"),

    path("projects_list/", ApiProject.as_view(), name = "api_project_list"),
    path("project_detail/", ApiProjectDetail.as_view(), name = "api_project_detail"),
    
    path("researchs_list/", ApiResearch.as_view(), name = "api_research_list"),
    path("research_detail/",ApiResearchDetail.as_view(), name = "api_research_detail" ),
    path("create_research/", ApiCreateResearch.as_view(), name = "api_create_research"),
    path("research_action/", ApiResearchAction, name = "api_research_action"),


]
