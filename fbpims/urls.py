"""fbpims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static 

from django.contrib import admin
from django.urls import path,include,re_path

from django.views.generic import TemplateView
from accounts.views import (CustomerAdminSignUpView,UserListView,RolesView,UserLogView,
                        UserDetailView,profileImage,CreateUserView,GroupView)
from core import views, front_views

urlpatterns = [
    # front page urls
    
    path("",front_views.IndexView.as_view(),name="index"),
    path("register/",TemplateView.as_view(template_name="frontpages/register.html"),name="register"),
    path("login/",TemplateView.as_view(template_name="frontpages/login.html"),name="login"),
    path("mydash/",TemplateView.as_view(template_name="frontpages/mydash.html"),name="mydash"),
    path("setting/",TemplateView.as_view(template_name="frontpages/settings.html"),name="setting"),
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
    path("blog-list-right/",TemplateView.as_view(template_name="frontpages/blog-list-right.html"),name="blog_list_right"),
    path("blog-detail-right/",TemplateView.as_view(template_name="frontpages/blog-details-right.html"),name="blog_details_right"),
    path("blog-grid/",TemplateView.as_view(template_name="frontpages/blog-grid.html"),name="blog_grid_f"),
    path("blog-grid-center/",TemplateView.as_view(template_name="frontpages/blog-grid-center.html"),name="blog_grid_center"),
    path("blog-grid-right/",TemplateView.as_view(template_name="frontpages/blog-grid-right.html"),name="blog_grid_right"),

    path("userprofile/",TemplateView.as_view(template_name="frontpages/userprofile.html"),name="userprofile"),
    path("mylistings/",TemplateView.as_view(template_name="frontpages/mylistings.html"),name="mylistings"),
    path("manged/",TemplateView.as_view(template_name="frontpages/manged.html"),name="manged"),
    path("orders/",TemplateView.as_view(template_name="frontpages/orders.html"),name="orders"),
    path("tips/",TemplateView.as_view(template_name="frontpages/tips.html"),name="tips"),
    path("payments/",TemplateView.as_view(template_name="frontpages/payments.html"),name="payments"),
    path("pricing/",TemplateView.as_view(template_name="frontpages/pricing.html"),name="pricing"),
    path("business-list/",TemplateView.as_view(template_name="frontpages/business-list.html"),name="bs_list"),
    path("business-list2/",TemplateView.as_view(template_name="frontpages/business-list2.html"),name="bs_list2"),
    path("bussiness-list3/",TemplateView.as_view(template_name="frontpages/business-list3.html"),name="bs_list3"),
    path("bussiness-list-right/",TemplateView.as_view(template_name="frontpages/business-list-right.html"),name="bs_list_right"),
    path("business-map/",TemplateView.as_view(template_name="frontpages/business-list-map.html"),name="bs_list_map"),
    path("business-map2/",TemplateView.as_view(template_name="frontpages/business-list-map2.html"),name="bs_list_map2"),
    path("business-map3/",TemplateView.as_view(template_name="frontpages/business-list-map3.html"),name="bs_list_map3"),
    path("categories/",TemplateView.as_view(template_name="frontpages/categories.html"),name="categories"),
    path("categories2/",TemplateView.as_view(template_name="frontpages/categories2.html"),name="categories2"),
    path("add-list2/",TemplateView.as_view(template_name="frontpages/ad-list2.html"),name="ad_list2"),
    path("personal-blog/",TemplateView.as_view(template_name="frontpages/personal-blog.html"),name="personal_blog"),
    
    path("not_found/",TemplateView.as_view(template_name="frontpages/404.html"),name="not_found"),
    path("faq/",TemplateView.as_view(template_name="frontpages/faq.html"),name="faq"),
    path("invoice/",TemplateView.as_view(template_name="frontpages/inovice.html"),name="invoice"),
    path("lockscreen/",TemplateView.as_view(template_name="frontpages/lockscreen.html"),name="lockscreen"),
    path("login2-/",TemplateView.as_view(template_name="frontpages/login-2.html"),name="login_2"),
    path("typography/",TemplateView.as_view(template_name="frontpages/typography.html"),name="typography"),
    path("underconstruction/",TemplateView.as_view(template_name="frontpages/underconstruction.html"),name="underconstruction"),
    
    # admin urls
    path('admin/', admin.site.urls),
    path("admin/signup/",CustomerAdminSignUpView.as_view(),name="signup"),
    path("admin/password_recovery/",TemplateView.as_view(template_name="admin/login_password_recover.html"),name="forgot_pass"),
    
    path('summernote/', include('django_summernote.urls')),
    # custom urls
    path("admin/create_user/<admin_type>/",CreateUserView.as_view(),name="create_user"),
    path("admin/users_list/",UserListView.as_view(),name="users_list"),
    path("admin/roles_list/",RolesView.as_view(),name="roles_list"),
    # path("admin/assign_roles/<userid>/<new_roles>",create_role,name="assign_roles"),
    path("admin/user_detail/<option>/<id>/",UserDetailView.as_view(),name="user_detail"),
    path("admin/ad_p_image/",profileImage,name="add_profile"),
    path("admin/categories/<option>/",views.CategoryView.as_view(),name="p_categories"),
    path("admin/create_category/<option>",views.CreateCategories.as_view(),name="create_category"),
    path("admin/category_edit/<option>/<cat_id>/",views.CategoryDetail.as_view(),name="edit_category"),
    path("admin/comp_profile/<option>/<id>/",views.CreateCompanyProfileView.as_view(),name="comp_profile"),
    path("admin/company_list/<option>/",views.CompaniesView.as_view(),name="companies"),
    path("admin/company_detail/<id>/",views.CompaniesDetailView.as_view(),name="company_detail"),
    path("admin/delete/<model_name>/<id>/",views.DeleteView.as_view(),name="delete"),
    path("admin/products_list/<user_type>/",views.AdminProductListView.as_view(),name="admin_products"),
    path("admin/create_product/",views.CreateProductView.as_view(),name="create_product"),
    path("admin/product_detail/<option>/<id>/",views.ProductDetailView.as_view(),name="product_detail"),
    path("admin/add_more_images/",views.AddProductImage.as_view(),name="add_product_image"),
    path("admin/create_price/",views.CreatePrice.as_view(),name="create_price"),
    path("admin/user_audit/",UserLogView.as_view(),name="useraudit"),
    path("admin/create_company_profile_al/<id>/",views.create_company_after_signup_view,name='ccp_al'),
    path("admin/manage_group/",GroupView.as_view(),name="group_view"),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)