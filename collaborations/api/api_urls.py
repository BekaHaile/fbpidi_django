from django.urls import path,include
from collaborations.views import PollIndex
from collaborations.api.api_views import (PollListApiView, PollDetailApiView, NewsListApiView, NewsDetailApiView, 
        EventListApiView, EventDetailApiView, EventNotifyApiView, ApiAnnouncementList, ApiAnnouncementDetail,
        ApiBlogList, ApiBlogDetail, ApiCreateBlogComment, ApiTenderList, ApiTenderDetail)

urlpatterns = [ 
    
    path("polls/", PollListApiView.as_view(), name = "client_polls" ),
    path("poll_detail/<id>/", PollDetailApiView.as_view(), name = "client_poll_detail" ),
    path('news/', NewsListApiView.as_view(), name = "client_news"),
    path('news_detail/<id>/', NewsDetailApiView.as_view(), name = 'client_news_detail'),
    path('events/', EventListApiView.as_view(), name = 'client_events'),
    path('event_detail/<id>/', EventDetailApiView.as_view(), name = "client_event_detail"),
    path('event_notify/<id>/', EventNotifyApiView, name= 'event_notify'),

    ## 
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
    # path("tender_application/", ApiApplyForTender, name= "api_tender_application"),
   
    # path("faq/",FaqList.as_view(),name="faq"),
    path("blog-list/",ApiBlogList.as_view(),name="api_blog_grid_right"),
    path("blog-details/",ApiBlogDetail.as_view(),name="api_blog_details"),
    path("blog-comment/",ApiCreateBlogComment,name="api_comment"),

    # path("vacancy-list/",VacancyList.as_view(),name="vacancy"),
    # path("vacancy-search/<id>",CategoryBasedSearch.as_view(),name="vacancy_search"),
    # path("vacancy-detail/<id>",VacancyMoreDetail.as_view(),name="vacancy_detail"),




################### Done
    # path("poll_detail/<id>/", PollDetail.as_view(), name = "poll_detail"),
    # ##News
    ## path("customer_news_list/", CustomerNewsList.as_view(), name = "customer_news_list"),
    ## path("customer_news_detail/<id>/", CustomerNewsDetail.as_view(), name = "customer_news_detail"),
    # ##Events
    ## path("customer_event_list/", CustomerEventList.as_view(), name = "customer_event_list"),
    ## path("customer_event_detail/<id>/", CustomerEventDetail.as_view(), name = "customer_event_detail"),
    ## path("event_participation/<id>/", EventParticipation.as_view(), name="event_participation"),

    
        
]
