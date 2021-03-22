from rest_framework import serializers
from accounts.api.serializers import UserSerializer, UserInfoSerializer
from collaborations.models import (PollsQuestion, PollsResult, Choices, News, NewsImages, Blog, BlogComment,
                                    Announcement, AnnouncementImages, Tender, TenderApplicant, Faqs, JobApplication, 
                                    JobCategory, Project, Research, ResearchProjectCategory, Vacancy, ForumQuestion,
                                    ForumComments, CommentReplay)
from company.models import Company, CompanyEvent
from company.api.serializers import CompanyFullSerializer, CompanyInfoSerializer


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
    no_of_votes = serializers.IntegerField(source='count_votes')
    company = CompanyInfoSerializer(read_only = True) 
    created_by = UserInfoSerializer(read_only = True)
    class Meta:
        model = PollsQuestion()
        fields = "__all__"
        
    
    
class PollDetailSerializer(serializers.ModelSerializer):
    no_of_choices = serializers.IntegerField(source='count_choices') # count_votes is an attribute in the model
    no_of_votes = serializers.IntegerField(source='count_votes')
    company = CompanyInfoSerializer(read_only = True)    
    choices = ChoiceSerializer(many = True, read_only=True, required=False)
    
    class Meta:
        model = PollsQuestion
        fields = '__all__'
    
    

class NewsListSerializer(serializers.ModelSerializer):
    images = serializers.CharField(source='get_single_image')  
    company = CompanyInfoSerializer(read_only = True)  
   
    class Meta:
        model = News
        fields = '__all__'
          
    

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImages
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    company = CompanyInfoSerializer(read_only = True) 
   
    class Meta:
        model = News
        fields = '__all__'
        
    def get_images(self, news):
        images = []
        for news_image in news.newsimages_set.all():
            images.append(news_image.image.url)
        
        return images
        
    

class EventListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_image')  
    company = CompanyInfoSerializer(read_only = True)  
   
    class Meta:
        model = CompanyEvent
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = "__all__"


class AnnouncementSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only = True)  

    class Meta:
        model = Announcement
        fields = "__all__"


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    images = serializers.SerializerMethodField('get_images')
    company = CompanyInfoSerializer(read_only = True)  
    class Meta:
        model = Announcement
        fields = "__all__"
    
    def get_images(self, announcement):
        images = []
        for announcement_image in announcement.announcementimages():
            images.append(announcement_image.image.url)
        return images        


class TenderSerializer(serializers.ModelSerializer):
    created_by = UserInfoSerializer(read_only=True)
    company = CompanyInfoSerializer(read_only=True)
    class Meta:
        model = Tender
        fields = "__all__"


class TenderApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenderApplicant
        fields = "__all__"


#sends only categoryName since it is only visible for customers
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ("id", "category_name", "category_name_am")


class VacancyListSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only =True)
    category_name = serializers.CharField(source='get_category_name')
    class Meta:
        model = Vacancy
        fields = '__all__'
    


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

