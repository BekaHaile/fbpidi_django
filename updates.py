import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fbpims.settings')
import django
django.setup()
from company.models import Company
from collaborations.models import News

def set_correct_company():
    for n in News.objects.all():
        print(f"for object  '{n.title}', company was  {n.company.company_name} \n" )
        n.company = n.user.get_company()
        n.save()
        print(f"after update  '{n.title}' company is set to {n.company.company_name} \n\n " )
        
if __name__ == '__main__':
    set_correct_company()
        
