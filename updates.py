import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from company.models import Company
from collaborations.models import News, Tender, PollsQuestion

def set_correct_company():
    # in every of the following models the .save() method sets the correct company object by using the company of the created_by field
    # check collaborations.models.py file
    for n in News.objects.all():
        n.save()
    for t in Tender.objects.all():
        t.save()
    for p in PollsQuestion.objects.all():
        p.save()
if __name__ == '__main__':
    # set_correct_company()
    for n in News.objects.all():
        print(n.title, " ", n.company.company_name, n.company.id)

        
