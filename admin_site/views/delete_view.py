import os
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView


# 
from product.models import *
from collaborations.models import *
from accounts.models import UserProfile
from admin_site.decorators import company_created,company_is_active
from company.models import (Company, CompanyEvent, HomePageSlider, InvestmentProject,
                             InvestmentCapital, Certificates,PowerConsumption,
                            Employees,JobOpportunities,FemalesInPosition,
                             EducationalStatus,SourceAmountIputs,
                             MarketTarget,MarketDestination)
from admin_site.views.views import record_activity

decorators = [never_cache, company_created(),company_is_active()]

@method_decorator(decorators,name='dispatch')
class DeleteAllView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        try:
            if self.kwargs['model_name'] == 'category':
                category = Category.objects.get(id=self.kwargs['id']) 
                record_activity(self.request.user,"Category","Category Deleted",category.id)
                category.delete()
                message = "Category Deleted"
                messages.success(self.request,message)
                return redirect("admin:categories")
            elif self.kwargs['model_name'] == 'sub_category':
                sub_category=SubCategory.objects.get(id=self.kwargs['id']) 
                record_activity(self.request.user,"SubCategory","Sub Category Deleted",sub_category.id)
                sub_category.delete()
                message = "Sub category Deleted"
                messages.success(self.request,message)
                return redirect("admin:sub_categories")
            elif self.kwargs['model_name'] == 'Brand':
                brand=Brand.objects.get(id=self.kwargs['id']) 
                record_activity(self.request.user,"Brand","Brand Deleted",brand.id)
                brand.delete()
                message = "Brand Deleted"
                messages.success(self.request,message)
                return redirect("admin:brands")
            elif self.kwargs['model_name'] == 'product':
                product = Product.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Product","Product Deleted",product.id)
                product.delete()
                message ="Product Deleted"
                messages.success(self.request,message)
                return redirect("admin:admin_products")
            elif self.kwargs['model_name'] == 'production_capacity':
                production_capacity = ProductionCapacity.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ProductionCapacity","ProductionCapacity Data Deleted",production_capacity.id)
                production_capacity.delete()
                message ="Production Capacity Deleted"
                messages.success(self.request,message)
                return redirect("admin:production_capacity")
            elif self.kwargs['model_name'] == 'anual_input_need':
                anual_input_need = AnnualInputNeed.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"AnnualInputNeed","Annual Input Need data Deleted",anual_input_need.id)
                anual_input_need.delete()
                message ="Annual Input Need Deleted"
                messages.success(self.request,message)
                return redirect("admin:anual_input_need")
            elif self.kwargs['model_name'] == 'input_demand_supply':
                input_demand_supply = InputDemandSupply.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"InputDemandSupply","Input Demand Supply data Deleted",input_demand_supply.id)
                input_demand_supply.delete()
                message ="Input Demand Supply Deleted"
                messages.success(self.request,message)
                return redirect("admin:demand_supply_list")
            elif self.kwargs['model_name'] == 'sales_performance':
                sales_performance = ProductionAndSalesPerformance.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ProductionAndSalesPerformance","Production & Sales Performance data Deleted",sales_performance.id)
                sales_performance.delete()
                message ="Production And Sales Performance Deleted"
                messages.success(self.request,message)
                return redirect("admin:sales_performance")
            elif self.kwargs['model_name'] == 'InvestmentCapital':
                investmentcapital = InvestmentCapital.objects.get(id=self.kwargs['id'])
                company_id  = investmentcapital.company.id
                record_activity(self.request.user,"InvestmentCapital","Investment Capital data Deleted",investmentcapital.id)
                investmentcapital.delete()
                message ="Investment Capital Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)
            elif self.kwargs['model_name'] == 'Certificates':
                certificate = Certificates.objects.get(id=self.kwargs['id'])
                company_id  = certificate.company.id
                record_activity(self.request.user,"Certificates","Certificates Deleted",certificate.id)
                certificate.delete()
                message ="Certificate Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)
            elif self.kwargs['model_name'] == 'Employees':
                obj = Employees.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"Employees","Employee data Deleted",obj.id)
                obj.delete()
                message ="Employee Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)
            elif self.kwargs['model_name'] == 'JobOpportunities':
                obj = JobOpportunities.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"JobOpportunities","Jobs Created data Deleted",obj.id)
                obj.delete()
                message ="Employee Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id) 
            elif self.kwargs['model_name'] == 'EducationalStatus':
                obj = EducationalStatus.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"EducationalStatus","Educational Status data Deleted",obj.id)
                obj.delete()
                message ="Employee Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id) 
            elif self.kwargs['model_name'] == 'FemalesInPosition':
                obj = FemalesInPosition.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"FemalesInPosition","Female Employees data Deleted",obj.id)
                obj.delete()
                message ="Employee Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id) 
            elif self.kwargs['model_name'] == 'SourceAmountIputs':
                obj = SourceAmountIputs.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"SourceAmountIputs","Source & Amount of inputs data Deleted",obj.id)
                obj.delete()
                message ="Source & Amount of Inputs Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)
            elif self.kwargs['model_name'] == 'MarketTarget':
                obj = MarketTarget.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"MarketTarget","Market Target data Deleted",obj.id)
                obj.delete()
                message ="Market Target data Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)    
            elif self.kwargs['model_name'] == 'MarketDestination':
                obj = MarketDestination.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"MarketDestination","Market Destination data Deleted",obj.id)
                obj.delete()
                message ="MarketDestination Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)
            elif self.kwargs['model_name'] == 'PowerConsumption':
                obj = PowerConsumption.objects.get(id=self.kwargs['id'])
                company_id  = obj.company.id
                record_activity(self.request.user,"PowerConsumption","Daily Power Consumption data Deleted",obj.id)
                obj.delete()
                message ="PowerConsumption Deleted"
                messages.success(self.request,message)
                return redirect("admin:update_company_info",pk=company_id)


            elif self.kwargs['model_name'] == 'packaging':
                packaging = ProductPackaging.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ProductPackaging","Product Packaging data Deleted",packaging.id)
                packaging.delete()
                message ="Product Packaging Deleted"
                messages.success(self.request,message)
                return redirect("admin:packaging")
            elif self.kwargs['model_name'] == 'slider_image':
                image = HomePageSlider.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"HomePageSlider","Company Slider Image Deleted",image.id)
                image.delete()
                message ="Slider Image Deleted"
                messages.success(self.request,message)
                return redirect("admin:slider_list")
            elif self.kwargs['model_name'] == 'investment_project':
                investment_project = InvestmentProject.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"InvestmentProject","Investment Project data Deleted",investment_project.id)
                investment_project.delete()
                message ="Investment Project Deleted"
                messages.success(self.request,message)
                return redirect("admin:project_list")


                # settings
            elif self.kwargs['model_name'] == 'CompanyDropdownsMaster':
                company_dropdown_master = CompanyDropdownsMaster.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"CompanyDropdownsMaster","Company lookup data Deleted",company_dropdown_master.id)
                company_dropdown_master.delete()
                message ="Company Lookup Item Deleted"
                messages.success(self.request,message)
                return redirect("admin:settings")
            elif self.kwargs['model_name'] == 'ProjectDropDownsMaster':
                project_dropdown_master = ProjectDropDownsMaster.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ProjectDropDownsMaster","Project lookup data Deleted",project_dropdown_master.id)
                project_dropdown_master.delete()
                message ="Project Lookup Item Deleted"
                messages.success(self.request,message)
                return redirect("admin:settings")
            elif self.kwargs['model_name'] == 'RegionMaster':
                region = RegionMaster.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"RegionMaster","Regions lookup data Deleted",region.id)
                region.delete()
                message ="Region Deleted"
                messages.success(self.request,message)
                return redirect("admin:settings")
            elif self.kwargs['model_name'] == 'uom_master':
                try:
                    region = UomMaster.objects.get(id=self.kwargs['id'])
                    record_activity(self.request.user,"UomMaster","Unit of Measurement lookup data Deleted",region.id)
                    region.delete()
                    message ="Unit of measurement Deleted"
                    messages.success(self.request,message)
                    return redirect("admin:settings")
                except Exception as e:
                    if "because they are referenced through restricted foreign keys" in e.args[0]:
                        messages.warning(self.request,"Unit of Measurement is Referenced, Can't be deleted")
                        return redirect("admin:settings")
                    else:
                        pass

            elif self.kwargs['model_name'] == 'Vacancy':
                vacancy = Vacancy.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Vacancy","Vacancy data Deleted",vacancy.id)
                vacancy.delete()
                message ="Vacancy Deleted"
                messages.success(self.request,message)
                if self.request.user.is_superuser:
                    return redirect("admin:super_Job_list")
                return redirect("admin:Job_list")
            elif self.kwargs['model_name'] == 'ForumQuestion':
                forum = ForumQuestion.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ForumQuestion","Forum data Deleted",forum.id)
                forum.delete()
                message ="Forum Deleted"
                messages.success(self.request,message)
                return redirect("forum_list")
            elif self.kwargs['model_name'] == 'ForumQuestionAdmin':
                forum = ForumQuestion.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ForumQuestion","Forum data Deleted",forum.id)
                forum.delete()
                message ="Forum Deleted"
                messages.success(self.request,message)
                return redirect("admin:forum_list")
            elif self.kwargs['model_name'] == 'ForumComments':
                announcement = ForumComments.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ForumComments","Forum comment Deleted",announcement.id)
                announcement.delete()
                return redirect("forum_list")
            elif self.kwargs['model_name'] == 'ForumCommentsAdmin':
                announcement = ForumComments.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ForumComments","Forum comment Deleted",forum.id)
                announcement.delete()
                message ="Forum Comment Deleted"
                messages.success(self.request,message)
                return redirect("admin:forum_comment_list")

            elif self.kwargs['model_name'] == 'ResearchProjectCategory':
                category = ResearchProjectCategory.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ResearchProjectCategory","Research Category data Deleted",category.id)
                category.delete()
                messages.success(self.request,"Research and project Category Deleted")
                return redirect("admin:settings")
            elif self.kwargs['model_name'] == 'PollsQuestion':
                poll = PollsQuestion.objects.get(id = self.kwargs['id'])
                record_activity(self.request.user,"PollsQuestion","Polls Data Deleted",poll.id)
                poll.delete()
                message = "Poll Deleted Successfully"
                return redirect('admin:admin_polls')
            elif self.kwargs['model_name'] == 'Choices':
                choice = Choices.objects.get(id = self.kwargs['id'])
                record_activity(self.request.user,"Choices","Poll Choices data Deleted",choice.id)
                choice.delete()
                message = "Poll choice Deleted Successfully"
                return redirect('admin:admin_polls')
            elif self.kwargs['model_name'] == 'BlogCommentsAdmin':
                blogcomments = BlogComment.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"BlogComment","Blog comments data Deleted",blogcomments.id)
                blogcomments.delete()
                message = "BlogComment Deleted"
                messages.success(self.request,message)
                return redirect("admin:blogComment_list")
            elif self.kwargs['model_name'] == 'Announcement':
                announcement = Announcement.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Announcement","Announcement data Deleted",announcement.id)
                announcement.delete()
                messages.success(self.request, "Announcement Deleted Successfully!")
                return redirect("admin:anounce_list")
            elif self.kwargs['model_name'] == 'AnnouncementImages':
                announcementimages = AnnouncementImages.objects.get(id=self.kwargs['id'])
                id =announcementimages.announcement.id
                record_activity(self.request.user,"AnnouncementImages","Announcement images data Deleted",announcementimages.id)
                announcementimages.delete()
                messages.success(self.request, "AnnouncementImages Deleted")
                return redirect(f"/admin/anounce-Detail/{id}/")
            elif self.kwargs['model_name'] == 'Research':
                research = Research.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Research","Research data Deleted",research.id)
                research.delete()
                message ="Research Deleted"
                messages.success(self.request,message)
                return redirect("admin:research_list") 
            elif self.kwargs['model_name'] == 'ResearchAttachment':
                researchimages = ResearchAttachment.objects.get(id=self.kwargs['id'])
                id =researchimages.research.id
                record_activity(self.request.user,"ResearchAttachment","Research file data Deleted",researchimages.id)
                researchimages.delete()
                message ="Research File Deleted"
                messages.success(self.request,message)
                return redirect("admin:research_detail",model_name="Research",id=id) 
            elif self.kwargs['model_name'] == 'ProjectClient':
                research = Project.objects.get(id=self.kwargs['id'])
                research.delete()
                messages.success(self.request,message)
                return redirect("project_list")
            elif self.kwargs['model_name'] == 'ResearchClient':
                research = Research.objects.get(id=self.kwargs['id'])
                research.delete()
                messages.success(self.request,message)
                return redirect("research_list")
            elif self.kwargs['model_name'] == 'CommentReplay':
                commentreplay = CommentReplay.objects.get(id=self.kwargs['id'])
                commentreplay.delete()
                return redirect("forum_list")
            elif self.kwargs['model_name'] == 'CommentReplayAdmin':
                commentreplay = CommentReplay.objects.get(id=self.kwargs['id'])
                commentreplay.delete()
                message ="comment Replay Deleted"
                messages.success(self.request,message)
                return redirect("admin:comment_replay_detail")
            elif self.kwargs['model_name'] == 'JobCategory':
                jobcategory = JobCategory.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"JobCategory","Vacancy category Deleted",jobcategory.id)
                jobcategory.delete()
                message ="Job category Deleted"
                messages.success(self.request,message)
                return redirect("admin:admin_JobCategory")
            elif self.kwargs['model_name'] == 'Blog':
                blog1 = Blog.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Blog","Blog data Deleted",blog1.id)
                blog1.delete()
                message ="Blog Deleted"
                messages.success(self.request,message)
                return redirect("admin:admin_Blogs")
            elif self.kwargs['model_name'] == 'Faqs':
                faqs = Faqs.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"Faqs","Faqs data Deleted",faqs.id)
                faqs.delete()
                message ="Faqs Deleted"
                messages.success(self.request,message)
                return redirect("admin:admin_Faqs") 
            elif self.kwargs['model_name'] == 'user_account':
                user = UserProfile.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"UserProfile","User data Deleted",user.id)
                user.delete()
                message ="User Deleted"
                messages.success(self.request,message)
                return redirect("admin:users_list")
            
            elif self.kwargs['model_name'] == 'company':
                company = Company.objects.get(id=self.kwargs['id'])
                company.delete()
                message ="Company Deleted"
            elif self.kwargs['model_name'] == 'product_image':
                pdimage = models.ProductImage.objects.get(id=self.kwargs['id'])
                record_activity(self.request.user,"ProductImage","Product Image data Deleted",pdimage.id)
                pdimage.delete()
                message ="Image Deleted"
                messages.success(self.request,message)
                return redirect("admin:product_detail",id=pdimage.product.id,option='view')
            elif self.kwargs['model_name'] == 'News':
                news = News.objects.get(id = self.kwargs['id']  )
                record_activity(self.request.user,"News","News data Deleted",news.id)
                news.delete() 
                messages.success(self.request,"News Deleted Successfully")
                return redirect("admin:news_list")
            elif self.kwargs['model_name'] == "NewsImage":  
                image = NewsImages.objects.get(id = self.kwargs['id']  )
                news = image.news
                record_activity(self.request.user,"NewsImages","News Image data Deleted",image.id)
                image.delete()
                messages.success(self.request,"Image Deleted Successfully!")
                return redirect(f"/admin/edit_news/{news.id}")
            elif self.kwargs['model_name'] == 'CompanyEvent':     
                event = CompanyEvent.objects.get(id = self.kwargs['id']  )
                company = event.company
                record_activity(self.request.user,"CompanyEvent","Event data Deleted",event.id)
                event.delete()
                messages.success(self.request,"Event Deleted Successfully!")
                return redirect("admin:admin_companyevent_list") 
            elif self.kwargs['model_name'] == "Document":
                document = Document.objects.get(id= self.kwargs['id'])
                category =document.category
                record_activity(self.request.user,"Document","Document data Deleted",document.id)
                document.delete()
                messages.success(self.request, "Document Deleted Successfully!")
                return render(self.request, f"admin/document/list_document_by_category.html", {'documents':Document.objects.filter(category = category), 'categories': Document.DOC_CATEGORY})
            elif self.kwargs['model_name'] == 'Tender':
                tender = Tender.objects.get(id = self.kwargs['id'])
                record_activity(self.request.user,"Tender","Tender data Deleted",tender.id)
                tender.delete()
                messages.success(self.request, "Tender Deleted Successfully!")
                return redirect("admin:tenders")   
            elif self.kwargs['model_name'] == 'phpg':
                phpg = PharmaceuticalProduct.objects.get(id = self.kwargs['id'])
                record_activity(self.request.user,"PharmaceuticalProduct","Product Group data Deleted",phpg.id)
                phpg.delete()
                messages.success(self.request, "Pharmaceutical Product Group Deleted Successfully!")
                return redirect("admin:settings")  
            elif self.kwargs['model_name'] == 'therapeutic_grp':
                tg = TherapeuticGroup.objects.get(id = self.kwargs['id'])
                record_activity(self.request.user,"TherapeuticGroup","Therapeutic group data Deleted",tg.id)
                tg.delete()
                messages.success(self.request, "Therapeutic Group Deleted Successfully!")
                return redirect("admin:settings")  
            else:
                return redirect("admin:error_404") 
        except Exception as e:
            print("#######Excetion While deleting ",e)
            return redirect("admin:error_404") 