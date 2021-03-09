import datetime
from django import forms
from django.contrib.gis import forms as gis_form
import floppyforms as fl_forms

from company.models import Company,CompanySolution,CompanyEvent,CompanyBankAccount,Bank
from admin_site.models import SubCategory,CompanyDropdownsMaster

from company.models import (Company,CompanySolution,CompanyEvent,
                             EventParticipants,
                             InvestmentCapital,)

# fields=(
#     'expansion_plan','expansion_plan_am','trade_license',
#             'working_hours','orgn_strct','lab_test_analysis','lab_test_analysis_am','lab_equipment',
#             'lab_equipment_am','outsourced_test_param','outsourced_test_param_am','certification',
#             'conducted_research','conducted_research_am','new_product_developed','new_product_developed_am',
#             'management_tools','electric_power','water_supply','telecom','marketing_department',
#             'e_commerce','active_database','waste_trtmnt_system','waste_trtmnt_system_am',
#             'efluent_trtmnt_plant','efluent_trtmnt_plant_am','env_mgmt_plan','source_of_energy',
#             'gas_carb_emision','gas_carb_emision_am','compound_allot','comunity_compliant', 
#             'comunity_compliant_am','env_focal_person','safety_profesional','notification_procedure', 
#             'university_linkage','university_linkage_am','recall_system','quality_defects_am', 
#             'quality_defects','gas_waste_mgmnt_measure','gas_waste_mgmnt_measure_am','support_required',
#             'company_condition',
# )

class LocationWidgetBuilder(fl_forms.gis.PointWidget, fl_forms.gis.BaseOsmWidget):
    pass

class CustomPointWidget(LocationWidgetBuilder):
    map_width = 900
    map_height = 300

class CompanyForm(forms.ModelForm):
    pass

YEAR_CHOICES=[('','Select Year'),]
YEAR_CHOICES += [(r,r) for r in range(1984, datetime.date.today().year+1)]

class InvestmentCapitalForm(forms.ModelForm):
    year = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model = InvestmentCapital
        fields = (
            'machinery_cost','building_cost','working_capital',
        )
        widgets = {
            'machinery_cost':forms.TextInput(
                    attrs={'class':'form-control','placeholder':'Machinery Cost',
                            'onkeyup':'isNumber("id_machinery_cost")'}),
            'building_cost':forms.TextInput(attrs={'class':'form-control','placeholder':'Building Cost',
                                            'onkeyup':'isNumber("id_building_cost")'}),
            'working_capital':forms.TextInput(attrs={'class':'form-control','placeholder':'Working Capital',
                                            'onkeyup':'isNumber("id_working_capital")'}),
        }

class CompanyDetailForm(forms.ModelForm):
    working_hours = forms.ModelChoiceField(
        empty_label="Select Working Hour",
        queryset=CompanyDropdownsMaster.objects.filter(chk_type="Working hours"),
        required=True,
        widget=forms.Select(attrs={'class':'form-control form-control-uniform'})
    )
    class Meta:
        model=Company
        fields=(
            'expansion_plan','expansion_plan_am',
            'orgn_strct','lab_test_analysis','lab_test_analysis_am','lab_equipment',
            'lab_equipment_am','outsourced_test_param','outsourced_test_param_am','certification',
            'conducted_research','conducted_research_am','new_product_developed','new_product_developed_am',
            'management_tools','electric_power','water_supply','telecom','marketing_department',
            'e_commerce','active_database','waste_trtmnt_system','waste_trtmnt_system_am',
            'efluent_trtmnt_plant','efluent_trtmnt_plant_am','env_mgmt_plan','source_of_energy',
            'gas_carb_emision','gas_carb_emision_am','compound_allot','comunity_compliant', 
            'comunity_compliant_am','env_focal_person','safety_profesional','notification_procedure', 
            'university_linkage','university_linkage_am','recall_system','quality_defects_am', 
            'quality_defects','gas_waste_mgmnt_measure','gas_waste_mgmnt_measure_am','support_required',
            'company_condition',
            )
        widgets = {
                'expansion_plan':forms.TextInput(attrs={'class':'summernote'}),
                'expansion_plan_am':forms.TextInput(attrs={'class':'summernote'}),
                'orgn_strct':forms.FileInput(),
            }

class CompanyProfileForm(forms.ModelForm):
    ownership = forms.ModelChoiceField(
        required=True,
        empty_label="Select Form Of Ownership",
        queryset=CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership'),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform',})
    )
    location = fl_forms.gis.PointField(widget=CustomPointWidget)

    class Meta:
        model = Company
        fields = (
            'name','name_am','logo','established_yr','category','trade_license',
            )
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in Amharic'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in English'}),
            'logo':forms.FileInput(attrs={'class':'form-input-styled'}),
            'established_yr':forms.TextInput(attrs={'class':'form-control','placeholder':'Established Year'}),
            'category':forms.SelectMultiple(attrs={'class':'form-control',}),
            'trade_license':forms.FileInput(attrs={'class':'form-input-styled'}),
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
        fields = ('__all__')
        widgets = {
            # Profile
            # 'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(English)'}),
            # 'company_name_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name(Amharic)'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address..'}),
            # 'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number...', "data-mask": "+251-99999-9999"}),
            # 'company_logo': forms.FileInput(attrs={'class': 'form-input-styled'}),
            # 'company_intro': forms.FileInput(attrs={'class': 'form-input-styled'}),
            # 'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            # 'established_year':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_year")','placeholder':'Year Of Establishement'}),
            # 'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            # 'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            # 'instagram_link':forms.TextInput(attrs={'class':'form-control','placeholder':'Main Products'}),
            # 'linkedin_link':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_capital")','placeholder':'Capital'}),
            # 'detail': forms.Textarea(attrs={'class': 'summernote'}),
            # 'detail_am': forms.Textarea(attrs={'class': 'summernote'}),
            # # 'color':forms.TextInput(attrs={'class':"form-control colorpicker-show-input",
            # #     'data-preferred-format':"hex",'data-fouc':'data-fouc', 'type': 'text'}),
            # 'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}),
            # 'twiter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter Link'}),
            # 'google_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Link'}),
            # 'pintrest_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pintrest Link'}),
        }
