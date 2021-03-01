from rest_framework import serializers
from accounts.api.serializers import UserSerializer
from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay)
from company.models import Company, CompanyEvent
from company.api.serializers import CompanyFullSerializer, CompanyInfoSerializer, CompanyDataSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    no_of_votes = serializers.SerializerMethodField('count_no_of_votes')
    serializers.SerializerMethodField()
    class Meta:
        model = Choices
        fields = "__all__"

    def count_no_of_votes(self, choice, **kwargs): 
        return PollsResult.objects.filter(choice=choice).count()
    

class PollListSerializer(serializers.ModelSerializer):
    no_of_choices = serializers.IntegerField(source='count_choices') # count_votes is an attribute in the model
    total_votes = serializers.IntegerField(source='count_votes')
    company_info = serializers.SerializerMethodField('get_company_info') 
    
    class Meta:
        model = PollsQuestion()
        fields = ('id','title', 'title_am', 'total_votes', 'no_of_choices' ,'company_info', 'user', 'timestamp' )
    
    def get_company_info(self, poll):
        company = poll.get_company()
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}

    
class PollDetailSerializer(serializers.ModelSerializer):
    no_of_choices = serializers.IntegerField(source='count_choices') # count_votes is an attribute in the model
    no_of_votes = serializers.IntegerField(source='count_votes')
    company_info = serializers.SerializerMethodField('get_company_info')     
    choices = ChoiceSerializer(many = True, read_only=True, required=False)
    
    class Meta:
        model = PollsQuestion
        fields = '__all__'
    
    def get_company_info(self, poll):
        company = poll.get_company()
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}


class NewsListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_single_image')  
    company_info = serializers.SerializerMethodField('get_company_info') 
   
    class Meta:
        model = News
        fields = '__all__'
          
    def get_company_info(self, news):
        company = news.get_company()
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImages
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    company_info = serializers.SerializerMethodField('get_company_info') 
   
    class Meta:
        model = News
        fields = '__all__'
        
    def get_images(self, news):
        images = []
        for news_image in news.newsimages_set.all():
            images.append(news_image.image.url)
        
        return images
        
    def get_company_info(self, news):
        company = news.get_company()
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}


class EventListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_image')  
    company_info = serializers.SerializerMethodField('get_company_info') 
   
    class Meta:
        model = CompanyEvent
        fields = "__all__"
    def get_company_info(self, event):
        company = event.company
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = serializers.SerializerMethodField('get_images')
    class Meta:
        model = Announcement
        fields = "__all__"
    
    def get_images(self, announcement):
        images = []
        for announcement_image in announcement.announcementimages():
            images.append(announcement_image.image.url)
        return images        


class TenderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company_info = serializers.SerializerMethodField('get_company_info')
    class Meta:
        model = Tender
        fields = "__all__"
    def get_company_info(self, tender):
        company = tender.get_company()
        return CompanyDataSerializer(company).data


class TenderApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderApplicant
        fields = "__all__"


#sends only categoryName since it is only visible for customers
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ("id", "categoryName", "categoryName_am")


class VacancyListSerializer(serializers.ModelSerializer):
    company_info = serializers.SerializerMethodField('get_company_info')
    category_name = serializers.CharField(source='get_category_name')
    class Meta:
        model = Vacancy
        fields = ('id', 'location', 'salary', 'category_name', 'category', 'employement_type', 'starting_date', 'ending_date',
                    'timestamp', 'job_title', 'job_title_am', 'closed', 'company_info' )
    def get_company_info(self, vacancy):
        return CompanyDataSerializer( vacancy.get_company()).data
 

class VacancyDetailSerializer(serializers.ModelSerializer):
    company_info = serializers.SerializerMethodField('get_company_info')
    category_name = serializers.CharField(source='get_category_name')
    class Meta:
        model = Vacancy
        fields ="__all__"

    def get_company_info(self, vacancy):
        return CompanyDataSerializer( vacancy.get_company()).data
 

class ResearchSerializer(serializers.ModelSerializer):
        category_name = serializers.CharField(source = 'get_category_name')
        class Meta:
            model = Research
            fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
        category_name = serializers.CharField(source = 'get_category_name')
        class Meta:
            model = Project
            fields = "__all__"


class ResearchProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchProjectCategory
        fields = "__all__"


class CommentReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReplay
        fields = "__all__"


class ForumCommentSerializer(serializers.ModelSerializer):
    no_or_replays = serializers.IntegerField(source='count_comment_replays',read_only=True)
    replays = CommentReplaySerializer(source = 'commentreplay', many = True, read_only = True)
    class Meta:
        model =  ForumComments
        fields = "__all__"


class ForumQuestionSerializer(serializers.ModelSerializer):
    no_of_comments = serializers.IntegerField(source='countComment', read_only=True)    
    class Meta:
        model = ForumQuestion
        fields = "__all__"


class ForumDetailSerializer(serializers.ModelSerializer):
    no_of_comments = serializers.IntegerField(source='countComment',read_only=True)
    comments_list = ForumCommentSerializer(source= 'comments', many = True, read_only = True)
    class Meta:
        model = ForumQuestion
        fields = "__all__"


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = "__all__"


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
