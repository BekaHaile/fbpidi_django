from rest_framework import serializers
# from collaborations.models import  PollsQuestion, PollsResult, Choices, News, NewsImage, 
from accounts.api.serializers import UserSerializer
from collaborations.models import PollsQuestion, PollsResult, Choices, News, NewsImages
    

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
        print(images)
        return images
        
    def get_company_info(self, news):
        company = news.get_company()
        return {'company_name':company.company_name, 'image':company.get_image(), 'phone_number':company.phone_number, 'location': company.location}

