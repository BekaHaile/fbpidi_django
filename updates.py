import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from company.models import Company
from collaborations.models import News, Tender, PollsQuestion, Project

def set_correct_company():
    # in every of the following models the .save() method sets the correct company object by using the company of the created_by field
    # check collaborations.models.py file
    for n in News.objects.all():
        n.save()
        print ("changed ",n.title)
    for t in Tender.objects.all():
        t.save()
        print ("changed ",t.title)
    for p in PollsQuestion.objects.all():
        p.save()
        print ("changed ",p.title)
    for pr in Project.objects.all():
        pr.save()
        print ("changed ",pr.title)
        
if __name__ == '__main__':
    set_correct_company()
    
