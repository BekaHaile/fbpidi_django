import datetime
from django import forms
from django.contrib.gis import forms as gis_form
import floppyforms as fl_forms

from admin_site.models import SubCategory,CompanyDropdownsMaster
from accounts.models import FbpidiUser
from company.models import *

# fields=(
#     'expansion_plan','expansion_plan_am','trade_license',
#             'working_hours','orgn_strct','lab_test_analysis','lab_test_analysis_am','lab_equipment',
#             'lab_equipment_am','outsourced_test_param','outsourced_test_param_am','certification',
#             'conducted_research','conducted_research_am','new_product_developed','new_product_developed_am',
#             'management_tools','electric_power','water_supply','telecom','marketing_department',
#             'e_commerce','active_database','waste_trtmnt_system','waste_trtmnt_system_am',
#             'efluent_treatment_plant','env_mgmt_plan','source_of_energy',
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

class CustomPointWidgetEdit(LocationWidgetBuilder):
    map_width = 560
    map_height = 300

class CompanyForm(forms.ModelForm):
    pass

YEAR_CHOICES=[('','Select Year'),]
YEAR_CHOICES += [(r,r) for r in range(2000, datetime.date.today().year+1)]

class InvestmentCapitalForm(forms.ModelForm):
    year_inv = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
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

class CertificateForm(forms.ModelForm):
    class Meta:
        model=Certificates
        fields = ('name','certificate',)
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Certificate Name'}),
            'certificate':forms.FileInput(attrs={'required':True})
        }

class EmployeesForm(forms.ModelForm):
    year_emp = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=Employees
        fields = ('employment_type','female','male',)
        widgets = {
            'employment_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class JobCreatedForm(forms.ModelForm):
    year_job = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=JobOpportunities
        fields = ('job_type','female','male',)
        widgets = {
            'job_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class EducationStatusForm(forms.ModelForm):
    year_edu = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=EducationalStatus
        fields = ('education_type','female','male',)
        widgets = {
            'education_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class FemalesInPositionForm(forms.ModelForm):
    year_fem = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=FemalesInPosition
        fields = ('high_position','med_position',)
        widgets = {
            'high_position':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_high_position")'}),
            'med_position':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_med_position")'}),
        }

class MarketDestinationForm(forms.ModelForm):
    year_destn = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=MarketDestination
        fields = ('domestic','export')
        widgets = {
            'domestic':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_domestic")'}),
            'export':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_export")'}),
        }

class MarketTargetForm(forms.ModelForm):
    year_target = forms.IntegerField(label="Year",
                widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=MarketTarget
        fields = ('further_proc_power','final_consumer','restaurant_and_hotels',
                    'institutions','epsa','hospitals','agents','wholesaler_distributor',
                    'retailer','other',)
        widgets = {
            'further_proc_power':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_further_proc_power")'}),
            'final_consumer':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_final_consumer")'}),
            'restaurant_and_hotels':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_restaurant_and_hotels")'}),
            'institutions':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_institutions")'}),
            'epsa':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_epsa")'}),
            'hospitals':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_hospitals")'}),
            'agents':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_agents")'}),
            'wholesaler_distributor':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_wholesaler_distributor")'}),
            'retailer':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_retailer")'}),
            'other':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_other")'}),
        }

class SourceAmountIputsForm(forms.ModelForm):
    year_src = forms.IntegerField(label="Year",widget=forms.Select(choices=YEAR_CHOICES,
                attrs={'class':'form-control form-control-uniform'}))
    class Meta:
        model=SourceAmountIputs
        fields = ('import_company','govt_suplied','purchase_from_farmer','purchase_from_union',
                    'purchase_from_agents','purchase_from_other')
        widgets = {
            'import_company':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_company")'}),
            'govt_suplied':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_govt_suplied")'}),
            'purchase_from_farmer':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_farmer")'}),
            'purchase_from_union':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_union")'}),
            'purchase_from_agents':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_agents")'}),
            'purchase_from_other':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_other")'}),
        }

class PowerConsumptionForm(forms.ModelForm):

    class Meta:
        model=PowerConsumption
        fields = ('day','installed_capacity','current_supply')
        widgets = {
            'day':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'installed_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_installed_capacity")'}),
            'current_supply':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_current_supply")'}),
        }

class CompanyDetailForm(forms.ModelForm):
    
    working_hours = forms.ModelChoiceField(
        label="Working hours per day",
        empty_label="Select Working Hour",
        queryset=CompanyDropdownsMaster.objects.filter(chk_type="Working hours"),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform','data-fouc':''}),
        required=True,
    )
    certification = forms.ModelMultipleChoiceField(
        label="Which certificate have you received?",
        queryset = CompanyDropdownsMaster.objects.filter(chk_type="Certifications"),
        required=True,
        widget=forms.SelectMultiple(attrs={'class':'form-control'})
    )
    management_tools = forms.ModelMultipleChoiceField(
        label="Which management tools do you apply?",
        queryset = CompanyDropdownsMaster.objects.filter(chk_type="Management Tools"),
        required=True,
        widget=forms.SelectMultiple(attrs={'class':'form-control'})
    )
    source_of_energy = forms.ModelChoiceField(
        label="What source of energy does the company use?",
        empty_label="Select Source of Energy",
        queryset = CompanyDropdownsMaster.objects.filter(chk_type="Source of Energy"),
        required=True,
        widget=forms.Select(attrs={'class':'form-control form-control-uniform','data-fouc':''})
    )
    support_required = forms.ModelChoiceField(
        label="What kind of support do you need to increase your production and market",
        empty_label="Select One",
        queryset = CompanyDropdownsMaster.objects.filter(chk_type="Areas of Major Challenges"),
        required=True,
        widget=forms.Select(attrs={'class':'form-control form-control-uniform','data-fouc':''})
    )
    company_condition = forms.ModelChoiceField(
        label="Status of processing/ industry facility.",
        empty_label="Select One Status",
        queryset = CompanyDropdownsMaster.objects.filter(chk_type="Industry Status Checklists"),
        required=False,
        widget=forms.Select(attrs={'class':'form-control form-control-uniform','data-fouc':''})
    )
    class Meta:
        model=Company
        fields=(
            'expansion_plan','expansion_plan_am',
            'orgn_strct','lab_test_analysis','lab_test_analysis_am','lab_equipment',
            'lab_equipment_am','outsourced_test_param','outsourced_test_param_am',
            'conducted_research','conducted_research_am','new_product_developed','new_product_developed_am',
            'electric_power','water_supply','telecom','marketing_department',
            'e_commerce','active_database','waste_trtmnt_system','waste_trtmnt_system_am',
            'efluent_treatment_plant','env_mgmt_plan',
            'gas_carb_emision','gas_carb_emision_am','compound_allot','comunity_compliant', 
            'comunity_compliant_am','env_focal_person','safety_profesional','notification_procedure', 
            'university_linkage','university_linkage_am','recall_system','quality_defects_am', 
            'quality_defects','gas_waste_mgmnt_measure','gas_waste_mgmnt_measure_am',
            
            )
        widgets = {
                'expansion_plan':forms.Textarea(attrs={'class':'summernote'}),
                'expansion_plan_am':forms.Textarea(attrs={'class':'summernote'}),
                'orgn_strct':forms.FileInput(),
                'lab_test_analysis':forms.Textarea(attrs={'class':'summernote'}),
                'lab_test_analysis_am':forms.Textarea(attrs={'class':'summernote'}),
                'lab_equipment':forms.Textarea(attrs={'class':'summernote'}),
                'lab_equipment_am':forms.Textarea(attrs={'class':'summernote'}),
                'outsourced_test_param':forms.Textarea(attrs={'class':'summernote'}),
                'outsourced_test_param_am':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research_am':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed_am':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system_am':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision_am':forms.Textarea(attrs={'class':'summernote'}),
                'comunity_compliant':forms.Textarea(attrs={'class':'summernote'}), 
                'comunity_compliant_am':forms.Textarea(attrs={'class':'summernote'}),
                'university_linkage':forms.Textarea(attrs={'class':'summernote'}),
                'university_linkage_am':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects_am':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure_am':forms.Textarea(attrs={'class':'summernote'}),
            }
class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model=CompanyAddress
        fields = ('region','city_town','subcity_zone','woreda','kebele','local_area',
                    'phone_number','fax','email','facebooklink','twiterlink','instagramlink',
                    'linkedinlink','googlelink')
        
        widgets = {
            'region':forms.TextInput(attrs={'class':'form-control','placeholder':'Region'}),
            'city_town':forms.TextInput(attrs={'class':'form-control','placeholder':'City/Town'}),
            'subcity_zone':forms.TextInput(attrs={'class':'form-control','placeholder':'Subcity/Zone'}),
            'woreda':forms.TextInput(attrs={'class':'form-control','placeholder':'Woreda'}),
            'kebele':forms.TextInput(attrs={'class':'form-control','placeholder':'Kebele'}),
            'local_area':forms.TextInput(attrs={'class':'form-control','placeholder':'Local Area'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number', "data-mask": "+251-99999-9999"}),
            'fax':forms.TextInput(attrs={'class':'form-control','placeholder':'Fax'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}),
            'facebooklink':forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook Account Link'}),
            'twiterlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Twitter Account Link'}),
            'instagramlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram Link'}),
            'linkedinlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Linkedin Link'}),
            'googlelink':forms.TextInput(attrs={'class':'form-control','placeholder':'Google Account Link'}),
        }

class CompanyProfileForm(forms.ModelForm):
    ownership = forms.ModelChoiceField(
        required=True,
        empty_label="Select Form Of Ownership",
        queryset=CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership'),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform',})
    )
    # location = fl_forms.gis.PointField(widget=CustomPointWidget)
    location = gis_form.PointField(widget=
        gis_form.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

    class Meta:
        model = Company
        fields = (
            'name','name_am','logo','established_yr','category','trade_license',
            )
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in Amharic'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in English'}),
            'logo':forms.FileInput(attrs={'class':''}),
            'established_yr':forms.TextInput(attrs={'class':'form-control','placeholder':'Established Year'}),
            'category':forms.SelectMultiple(attrs={'class':'form-control',}),
            'trade_license':forms.FileInput(attrs={'class':''}),
        }


class CompanyProfileForm_Superadmin(forms.ModelForm):
    ownership = forms.ModelChoiceField(
        required=True,
        empty_label="Select Form Of Ownership",
        queryset=CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership'),
        widget=forms.Select(attrs={'class':'form-control form-control-uniform',})
    )
    # location = fl_forms.gis.PointField(widget=CustomPointWidget)
    location = gis_form.PointField(widget=
        gis_form.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

    class Meta:
        model = Company
        fields = (
            'contact_person','name','name_am','logo','established_yr','category','trade_license',
            )
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in Amharic'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in English'}),
            'logo':forms.FileInput(attrs={'class':''}),
            'established_yr':forms.TextInput(attrs={'class':'form-control','placeholder':'Established Year'}),
            'category':forms.SelectMultiple(attrs={'class':'form-control',}),
            'trade_license':forms.FileInput(attrs={'class':''}),
        }

    def __init__(self,*args,**kwargs):
        super(CompanyUpdateForm,self).__init__(*args,**kwargs)
        # self.fields['contact_person'].queryset = FbpidiUser.objects.filter(contact_person=)

class CompanyUpdateForm(forms.ModelForm):
     
    # company_condition = forms.ModelChoiceField(
    #     label="Status of processing/ industry facility.",
    #     empty_label="Select One Status",
    #     queryset = CompanyDropdownsMaster.objects.filter(chk_type="Industry Status Checklists"),
    #     required=False,
    #     widget=forms.Select(attrs={'class':'form-control form-control-uniform','data-fouc':''})
    # )

    class Meta:
        model=Company
        fields=('name','name_am','logo','established_yr','category','ownership_form','trade_license',
            'expansion_plan','expansion_plan_am','geo_location',
            'orgn_strct','certification','management_tools','working_hours',
            'lab_test_analysis','lab_test_analysis_am','lab_equipment',
            'lab_equipment_am','outsourced_test_param','outsourced_test_param_am',
            'conducted_research','conducted_research_am','new_product_developed','new_product_developed_am',
            'electric_power','water_supply','telecom','marketing_department','source_of_energy',
            'e_commerce','active_database','waste_trtmnt_system','waste_trtmnt_system_am',
            'efluent_treatment_plant','env_mgmt_plan',
            'gas_carb_emision','gas_carb_emision_am','compound_allot','comunity_compliant', 
            'comunity_compliant_am','env_focal_person','safety_profesional','notification_procedure', 
            'university_linkage','university_linkage_am','recall_system','quality_defects_am', 
            'quality_defects','gas_waste_mgmnt_measure','gas_waste_mgmnt_measure_am','support_required',
            
            )
        widgets = {
                'expansion_plan':forms.Textarea(attrs={'class':'summernote'}),
                'expansion_plan_am':forms.Textarea(attrs={'class':'summernote'}),
                'orgn_strct':forms.FileInput(),
                'geo_location':gis_form.OSMWidget(attrs={'map_width': 500, 'map_height': 250}),
                'lab_test_analysis':forms.Textarea(attrs={'class':'summernote'}),
                'lab_test_analysis_am':forms.Textarea(attrs={'class':'summernote'}),
                'lab_equipment':forms.Textarea(attrs={'class':'summernote'}),
                'lab_equipment_am':forms.Textarea(attrs={'class':'summernote'}),
                'outsourced_test_param':forms.Textarea(attrs={'class':'summernote'}),
                'outsourced_test_param_am':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research_am':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed_am':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system_am':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision_am':forms.Textarea(attrs={'class':'summernote'}),
                'comunity_compliant':forms.Textarea(attrs={'class':'summernote'}), 
                'comunity_compliant_am':forms.Textarea(attrs={'class':'summernote'}),
                'university_linkage':forms.Textarea(attrs={'class':'summernote'}),
                'university_linkage_am':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects_am':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure_am':forms.Textarea(attrs={'class':'summernote'}),
            }
        
    def __init__(self,*args,**kwargs):
        super(CompanyUpdateForm,self).__init__(*args,**kwargs)
        self.fields['certification'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Certifications")
        self.fields['source_of_energy'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Source of Energy")
        self.fields['support_required'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Areas of Major Challenges")
        self.fields['management_tools'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Management Tools")
        self.fields['working_hours'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Working hours")
        self.fields['working_hours'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Working hours")
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
  

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
    class Meta:
        model=CompanyEvent
        fields = ('title','title_am','description','description_am','image', 'start_date', 'end_date')
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
