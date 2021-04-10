
import datetime
from django.http import HttpResponse
from django.views.generic import View,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.db.models import *

from company.render import render_to_pdf 
from company.models import *

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
             'today': datetime.date.today(), 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf_templates/pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

# def render_pdf_view(request):
#     template_path = 'admin/report/pdf_template.html'
#     company = Company.objects.get(id=self.request.POST['pk'])
#     inv_cap =  InvestmentCapital.objects.filter(company=company).annotate(
#                     machinery = Sum('machinery_cost'),
#                     building = Sum('building_cost'),
#                     working = Sum('working_capital')
#                 )
    
#     context = {'company':company,'inv_capital':inv_cap}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#     html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
    

class GenerateCompanyToPDF(LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        context = {}
        template = get_template('admin/report/pdf_template.html')
        company = Company.objects.get(id=self.request.POST['pk'])
        inv_cap =  InvestmentCapital.objects.filter(company=company).annotate(
                        machinery = Sum('machinery_cost'),
                        building = Sum('building_cost'),
                        working = Sum('working_capital')
                    )
        today = datetime.datetime.today()
        this_year = today.year
        ethio_year = (this_year-8)
        context = {'company':company,'inv_capital':inv_cap,'years':{'this_yr':ethio_year-1,'last_yr':ethio_year-2,'prev_yr':ethio_year-3}}
        print(context)
        html = template.render(context)
        pdf = render_to_pdf('admin/report/pdf_template.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Template_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template.loader import render_to_string

# from weasyprint import HTML

# def html_to_pdf_view(request):
#     paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#     html_string = render_to_string('admin/report/template.html', {'paragraphs': paragraphs})

#     html = HTML(string=html_string)
#     html.write_pdf(target='mypdf.pdf');

#     fs = FileSystemStorage('/')
#     with fs.open('mypdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#         return response

#     return response