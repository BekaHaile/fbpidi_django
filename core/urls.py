from django.urls import path,include
from django.views.generic import TemplateView

from core.views import (IndexView,ProfileView,ProductDetailView,ProductByCategoryView,
                    ProductByMainCategory,MnfcCompanyByMainCategory,SupCompanyByMainCategory )
from collaborations.views import BlogList,BlogDetail,FaqList
from accounts.views import CustomerSignUpView

# busines-meditation/,tips/,orders
urlpatterns = [
    path("",IndexView.as_view(),name='index'),
    path("blog-grid-right/",BlogList.as_view(),name="blog_grid_right"),
    path("blog-detail-right/<id>",BlogDetail.as_view(),name="blog_details"),
    path("product-detail/<id>",ProductDetailView.as_view(),name="product_detail"),
    path("product-by-category/<cat_id>/",ProductByCategoryView.as_view(),name="product_category"),
    path("product-by-main-category/<option>/",ProductByMainCategory.as_view(),name="product_category_main"),
    path("man_comp-by-main-category/<option>/",MnfcCompanyByMainCategory.as_view(),name="manufac_category_main"),
    path("sup_comp-by-main-category/<option>/",SupCompanyByMainCategory.as_view(),name="suplier_category_main"),
    path("mydash/",ProfileView.as_view(),name="mydash"),
    path("",include("accounts.urls")),



    # path("login/",TemplateView.as_view(template_name="frontpages/login.html"),name="login"),
    # unused urls those will be removed in the futurepath("register/",CustomerSignUpView.as_view(),name="register"),
    path("faq/",FaqList.as_view(),name="faq"),
    path("vacancy-list/",TemplateView.as_view(template_name="frontpages/vacancy_list.html"),name="tips"),
    
    path("accounts/",include("django.contrib.auth.urls")), 
    path("test/",TemplateView.as_view(template_name="frontpages/date_piker.html"),name="Test"),
    path("setting/",TemplateView.as_view(template_name="frontpages/settings.html"),name="setting"),
    # path("login/",TemplateView.as_view(template_name="frontpages/login.html"),name="login"),
    path("mydash/",ProfileView.as_view(),name="mydash"),
    path("Job-detail/",TemplateView.as_view(template_name="admin/pages/job_detail.html"),name="Job_detail"),
    #path("Job-form/",TemplateView.as_view(template_name="admin/pages/job_form.html"),name="Job_form"),
    path("job-list/",TemplateView.as_view(template_name="admin/pages/job_list.html"),name="Job_list"),
    path("myfavorite/",TemplateView.as_view(template_name="frontpages/myfavorite.html"),name="favorite"),
    path("forgot/",TemplateView.as_view(template_name="frontpages/forgot.html"),name="forgot"),
    path("add-list/",TemplateView.as_view(template_name="frontpages/ad-list.html"),name="ad_list"),
    path("about/",TemplateView.as_view(template_name="frontpages/about.html"),name="about"),
    path("contact/",TemplateView.as_view(template_name="frontpages/contact.html"),name="contact"),
    path("widgets/",TemplateView.as_view(template_name="frontpages/widgets.html"),name="widgets"),
    path("widgets-vertical/",TemplateView.as_view(template_name="frontpages/widgets-verticalscroll.html"),name="widgets_vert"),
    path("widgets-carousel/",TemplateView.as_view(template_name="frontpages/widgets-carousel.html"),name="widgets_car"),
    path("busines-education/",TemplateView.as_view(template_name="frontpages/business.html"),name="bs"),
    path("busines-meditation/",TemplateView.as_view(template_name="frontpages/business-2.html"),name="bs_2"),
    path("busines-realstate/",TemplateView.as_view(template_name="frontpages/business-3.html"),name="bs_3"),
    path("busines-restoraunt/",TemplateView.as_view(template_name="frontpages/business-4.html"),name="bs_4"),
    path("busines-bakery/",TemplateView.as_view(template_name="frontpages/business-5.html"),name="bs_5"),
    path("busines-beuty-spa/",TemplateView.as_view(template_name="frontpages/business-6.html"),name="bs_6"),
    path("business-authomobiles/",TemplateView.as_view(template_name="frontpages/business-right.html"),name="bs_right"),
    path("blog-list-center/",TemplateView.as_view(template_name="frontpages/blog-list-center.html"),name="blog_list_center"),
    path("blog-detail-center/",TemplateView.as_view(template_name="frontpages/blog-details-center.html"),name="blog_details_center"),
    path("blog-list/",TemplateView.as_view(template_name="frontpages/blog-list.html"),name="blog_list"),
    path("blog-detail/",TemplateView.as_view(template_name="frontpages/blog-details.html"),name="blog_details"),
    #path("blog-list-right/",TemplateView.as_view(template_name="frontpages/blog-list-right.html"),name="blog_list_right"),
    #path("blog-detail-right/",TemplateView.as_view(template_name="frontpages/blog-details-right.html"),name="blog_details_right"),
    path("blog-grid/",TemplateView.as_view(template_name="frontpages/blog-grid.html"),name="blog_grid_f"),
    path("blog-grid-center/",TemplateView.as_view(template_name="frontpages/blog-grid-center.html"),name="blog_grid_center"),
    #path("blog-grid-right/",TemplateView.as_view(template_name="frontpages/blog-grid-right.html"),name="blog_grid_right"),

    path("userprofile/",TemplateView.as_view(template_name="frontpages/userprofile.html"),name="userprofile"),
    path("mylistings/",TemplateView.as_view(template_name="frontpages/mylistings.html"),name="mylistings"),
    path("manged/",TemplateView.as_view(template_name="frontpages/manged.html"),name="manged"),
    path("orders/",TemplateView.as_view(template_name="frontpages/orders.html"),name="orders"),
    path("tips/",TemplateView.as_view(template_name="frontpages/tips.html"),name="tips"),
    path("payments/",TemplateView.as_view(template_name="frontpages/payments.html"),name="payments"),
    path("pricing/",TemplateView.as_view(template_name="frontpages/pricing.html"),name="pricing"),
    path("business-list/",TemplateView.as_view(template_name="frontpages/business-list.html"),name="bs_list"),
    path("business-list2/",TemplateView.as_view(template_name="frontpages/business-list2.html"),name="bs_list2"),
    path("business-list3/",TemplateView.as_view(template_name="frontpages/business-list3.html"),name="bs_list3"),
    path("business-list-right/",TemplateView.as_view(template_name="frontpages/business-list-right.html"),name="bs_list_right"),
    path("business-map/",TemplateView.as_view(template_name="frontpages/business-list-map.html"),name="bs_list_map"),
    path("business-map2/",TemplateView.as_view(template_name="frontpages/business-list-map2.html"),name="bs_list_map2"),
    path("business-map3/",TemplateView.as_view(template_name="frontpages/business-list-map3.html"),name="bs_list_map3"),
    path("categories/",TemplateView.as_view(template_name="frontpages/categories.html"),name="categories"),
    path("categories2/",TemplateView.as_view(template_name="frontpages/categories2.html"),name="categories2"),
    path("add-list2/",TemplateView.as_view(template_name="frontpages/ad-list2.html"),name="ad_list2"),
    path("personal-blog/",TemplateView.as_view(template_name="frontpages/personal-blog.html"),name="personal_blog"),
    
    path("not_found/",TemplateView.as_view(template_name="frontpages/404.html"),name="not_found"),
    
    path("invoice/",TemplateView.as_view(template_name="frontpages/inovice.html"),name="invoice"),
    path("lockscreen/",TemplateView.as_view(template_name="frontpages/lockscreen.html"),name="lockscreen"),
    path("login2-/",TemplateView.as_view(template_name="frontpages/login-2.html"),name="login_2"),
    path("typography/",TemplateView.as_view(template_name="frontpages/typography.html"),name="typography"),
    path("underconstruction/",TemplateView.as_view(template_name="frontpages/underconstruction.html"),name="underconstruction"),
    path("check_comp/",TemplateView.as_view(template_name="frontpages/company/index.html"),name="chcmp"),
]
