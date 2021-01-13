from django import forms
from company.models import Company,CompanySolution

class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = (
            # Company Profile
                'company_name', 'company_name_am', 'email', 'phone_number','city','postal_code',
                  'detail', 'detail_am', 'company_logo', 'location', 'company_intro',
                  'number_of_employees','established_year','certification','products','capital',
            # trade capacity
            'incoterms','incoterms_am','terms_of_payment','average_lead_time','average_lead_time_am',
            'no_trading_staff','export_yr','export_percentage','main_market','main_market_am',
            'nearest_port','nearest_port_am',
            # production capacity
            'r_and_d_capacity','r_and_d_capacity_am','no_of_rnd_staff','no_production_lines',
            'anual_op_value','anual_op_main_products','anual_op_main_products_am',
            )
        widgets = {
            # Profile
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(English)'}),
            'company_name_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(Amharic)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address..'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number...', "data-mask": "+251-99999-9999"}),
            'company_logo': forms.FileInput(attrs={'class': 'form-input-styled'}),
            'company_intro': forms.FileInput(attrs={'class': 'form-input-styled'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'number_of_employees':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_number_of_employees")','placeholder':'Number Of Employees'}),
            'established_year':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_year")','placeholder':'Year Of Establishement'}),
            'certification':forms.TextInput(attrs={'class':'form-control','placeholder':'Management System Certification'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'products':forms.TextInput(attrs={'class':'form-control','placeholder':'Main Products'}),
            'capital':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_capital")','placeholder':'Capital'}),
            'detail': forms.Textarea(attrs={'class': 'summernote'}),
            'detail_am': forms.Textarea(attrs={'class': 'summernote'}),
            # Trade Capacity
            'incoterms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Incoterms(English)'}),
            'incoterms_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Incoterms(Amharic)'}),
            'average_lead_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Average Lead Time(English)'}),
            'average_lead_time_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Average Lead Time(Amharic)'}),
            'no_trading_staff': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_no_trading_staff")', 'placeholder': 'Number Of Trading Staff'}),
            'terms_of_payment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Methods'}),
            'export_yr': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_export_yr")', 'placeholder': 'Export Year'}),
            'export_percentage': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_export_percentage")', 'placeholder': 'Export Percentage'}),
            'main_market': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Main Market(English)'}),
            'main_market_am': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Main Market(Amharic)'}),
            'nearest_port': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nearest Port(English)'}),
            'nearest_port_am': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nearest Port(Amharic)'}),
            # 'import_export':forms.CheckboxInput(attrs={'class':"form-check-input-styled"}),
            # production capacity
            'r_and_d_capacity': forms.TextInput(attrs={'class': 'form-control','placeholder': 'R&D Capacity(English)'}),
            'r_and_d_capacity_am': forms.TextInput(attrs={'class': 'form-control','placeholder': 'R&D Capacity(Amharic)'}),
            'no_of_rnd_staff': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_no_of_rnd_staff")','placeholder': 'Number of R&D Staff'}),
            'no_production_lines': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_no_production_lines")','placeholder': 'Number Of Production Lines'}),
            'anual_op_value': forms.TextInput(attrs={'class': 'form-control','onkeyup':'isNumber("id_anual_op_value")','placeholder': 'Anual Output Value'}),
            'anual_op_main_products': forms.Textarea(attrs={'class': 'summernote'}),
            'anual_op_main_products_am': forms.Textarea(attrs={'class': 'summernote'}),
        }


class CompanySolutionForm(forms.ModelForm):

    class Meta:
        model = CompanySolution
        fields = ('title','title_am','description','description_am','link',)
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (English)'}),
            'title_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (Amharic)'}),
            'description': forms.Textarea(attrs={'class': 'summernote'}),
            'description_am': forms.Textarea(attrs={'class': 'summernote'}),
            'link':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Required Link'}),
        }