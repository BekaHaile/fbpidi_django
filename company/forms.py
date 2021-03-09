from django import forms
from company.models import Company,CompanySolution,CompanyEvent,CompanyBankAccount,Bank
from admin_site.models import SubCategory

from company.models import Company,CompanySolution,CompanyEvent, EventParticipants

class CompanyForm(forms.ModelForm):
    # color = forms.CharField(label='Company Theme Color',
    #     widget=forms.TextInput(attrs={'class':"form-control colorpicker-show-input",
    #                 'data-preferred-format':"hex",'data-fouc':'data-fouc', 'type': 'text'}))
    product_category = forms.ModelChoiceField(
        empty_label="Select Main Product Type",
        queryset=SubCategory.objects.all(),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),
        required=True
    )
    class Meta:
        model = Company
        fields = (
            # Company Profile
                'company_name', 'company_name_am', 'email', 'phone_number','city','postal_code',
                  'detail', 'detail_am', 'company_logo', 'location', 'company_intro','color',
                  'number_of_employees','established_year','certification','capital',
                #   'facebook_link','twitter_link','google_link','pintrest_link'
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
            # 'product_category':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'capital':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_capital")','placeholder':'Capital'}),
            'detail': forms.Textarea(attrs={'class': 'summernote'}),
            'detail_am': forms.Textarea(attrs={'class': 'summernote'}),
            'color':forms.TextInput(attrs={'class':"form-control colorpicker-show-input",
                    'data-preferred-format':"hex",'data-fouc':'data-fouc', 'type': 'text'}),
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
        fields = ('title','title_am','description','description_am','link','image',)
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (English)'}),
            'title_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title (Amharic)'}),
            'description': forms.Textarea(attrs={'class': 'summernote'}),
            'description_am': forms.Textarea(attrs={'class': 'summernote'}),
            'image': forms.FileInput(attrs={'class': 'form-input-styled'}),
            'link':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Required Link'}),
        }

class CompanyEventForm(forms.ModelForm):
    STATUS_CHOICE = [ ('Upcoming', 'Upcoming'),('Open', 'Open' )]
    image = forms.FileField(allow_empty_file=True, required=False, widget= forms.FileInput(attrs={'class': 'form-input-styled',}) )
    status = forms.ChoiceField(choices = STATUS_CHOICE, required=True, widget=forms.Select(attrs={'type': 'dropdown'}),)

    class Meta:
        model=CompanyEvent
        fields = ('title','title_am','description','description_am','image','status', 'start_date', 'end_date')
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name (English)'}),
            'title_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name (Amharic)'}),
            'description': forms.Textarea(attrs={'class': 'summernote'}),
            'description_am': forms.Textarea(attrs={'class': 'summernote'}),
            'start_date': forms.DateTimeInput(attrs={'class':"form-control daterange-single"}),
            'end_date': forms.DateTimeInput(attrs={'class':"form-control daterange-single"}),
            'image': forms.FileInput(attrs={'class': 'form-input-styled',}),

        }

class EventParticipantForm(forms.ModelForm):
    notify_in = forms.IntegerField(required=False,)  
    class Meta:
        model=EventParticipants
        fields = ('patricipant_email', 'notify_in')
        widgets = {
            'patricipant_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address..'}),
             'notify_in':forms.NumberInput(attrs={'class': 'form-control', 'max':'10', 'placeholder':"Notify me before -- days" })
        }

class CompanyBankAccountForm(forms.ModelForm):
    bank = forms.ModelChoiceField(empty_label="Choose Bank", queryset=Bank.objects.all(),widget=forms.Select(attrs={'class':'form-control form-control-uniform'}),required=True)

    class Meta:
        model = CompanyBankAccount
        fields = ('bank', 'account_number')
        widgets = {
            'bank':forms.Select(),
            'account_number':forms.TextInput( attrs = {'class': 'form-control', 'placeholder': 'Valid bank account (for the selected bank)'}),
        }

        
# class FbpidiCompanyForm()
class FbpidiCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = (
            # Company Profile
                  'company_name', 'company_name_am', 'email', 'phone_number','city','postal_code',
                  'detail', 'detail_am', 'company_logo', 'location', 'company_intro',
                  'established_year','linkedin_link','instagram_link',
                  'facebook_link','twiter_link','google_link','pintrest_link',
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
            'established_year':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_year")','placeholder':'Year Of Establishement'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'instagram_link':forms.TextInput(attrs={'class':'form-control','placeholder':'Main Products'}),
            'linkedin_link':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_capital")','placeholder':'Capital'}),
            'detail': forms.Textarea(attrs={'class': 'summernote'}),
            'detail_am': forms.Textarea(attrs={'class': 'summernote'}),
            # 'color':forms.TextInput(attrs={'class':"form-control colorpicker-show-input",
            #     'data-preferred-format':"hex",'data-fouc':'data-fouc', 'type': 'text'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}),
            'twiter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter Link'}),
            'google_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Link'}),
            'pintrest_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pintrest Link'}),
        }
