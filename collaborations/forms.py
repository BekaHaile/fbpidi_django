from django import forms
from collaborations.models import Blog,BlogComment
from django_summernote.widgets import SummernoteWidget

from collaborations.models import Faqs

class CreateFaqs(forms.ModelForm):
    
    
    questions_am = forms.CharField(label='questions_am',widget=forms.TextInput(
    	attrs={'placeholder': 'question in amharic'}))

    class Meta:
        model = Faqs
        fields = ('questions', 'questions_am',
                  'answers', 'answers_am')
        widgets = {'answers': SummernoteWidget,'answers_am': SummernoteWidget}


class CreateBlogs(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title', 'tag', 'content','publish','blogImage','title_am','tag_am','content_am')
        widgets = {'content': SummernoteWidget,'content_am': SummernoteWidget}


class CreateBlogComment(forms.ModelForm):
	
	class Meta:
		model = BlogComment
		fields = ('content',)





