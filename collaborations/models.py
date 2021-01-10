from django.db import models
from django.conf import settings




class PollsQuestion(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    title = models.CharField( max_length=200, verbose_name="Poll title (English)" )
    title_am = models.CharField( max_length=200, verbose_name="Poll title(Amharic)" )
    description = models.TextField( verbose_name="Poll Description(English)" )
    description_am = models.TextField( verbose_name="Poll Description(Amharic)" )
    timestamp = models.DateTimeField(auto_now_add=True)
    choices = models.ManyToManyField('Choices',related_name='choices',default="",)

    def __str__(self):
        return self.title

class Choices (models.Model):
    choice_name = models.CharField( max_length=200, verbose_name="Choice name (English)" )
    choice_name_am = models.CharField( max_length=200, verbose_name="Choice name(Amharic)" )
    description = models.TextField( verbose_name="Choice Description(English)" )
    description_am = models.TextField( verbose_name="Choice Description(Amharic)" )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice_name


class PollsResult(models.Model):    
    poll = models.ForeignKey(PollsQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    remark = models.CharField( max_length=200,verbose_name= "Any remarks the user may have" )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poll.title}'s Result "

