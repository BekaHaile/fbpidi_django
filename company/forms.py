import datetime
from django import forms
from django.contrib.gis import forms as gis_form
from django.db.models import OuterRef,Exists
from django.db.transaction import atomic
from django_summernote.fields import SummernoteWidget

from PIL import Image

from mapwidgets.widgets import GooglePointFieldWidget

from admin_site.models import CompanyDropdownsMaster
from accounts.models import UserProfile
from company.models import *

    
def return_years(company):
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if month <= 7 and day < 8 or month <= 7:
        current_year = gc_year-9
    else:
        current_year = gc_year - 8
    YEAR_CHOICES=[('','Select Year'),]
    YEAR_CHOICES += [(r,r) for r in range(company.established_yr, current_year+1)]
    return YEAR_CHOICES

def in_between(x,min,max):
    return ((x-min)*(x-max) <= 0)

def return_year_with_quarteryear(company):
    current_year = 0
    gc_year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if in_between(month,10,12) or in_between(month,1,3) or in_between(month,4,6):
        current_year = gc_year-8
    else:
        current_year = gc_year - 9
    YEAR_CHOICES=[('','Select Year'),]
    YEAR_CHOICES += [(r,r) for r in range(company.established_yr, current_year+1)]
    return YEAR_CHOICES

class InvestmentCapitalForm(forms.ModelForm):
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

    # year_emp = forms.IntegerField(label="Year",widget=forms.Select(choices=return_years(company_obj),attrs={
    #             'class':'form-control form-control-uniform'}))
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(EmployeesForm,self).__init__(*args,**kwargs)
        self.fields['year_emp'].widget = forms.Select(choices = return_years(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
    
    class Meta:
        model=Employees
        fields = ('year_emp','employment_type','female','male')
        widgets = {
            'employment_type':forms.Select(attrs={'class':'form-control form-control-uniform','disabled':'true'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class JobCreatedForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(JobCreatedForm,self).__init__(*args,**kwargs)
        self.fields['year_job'].widget = forms.Select(choices = return_year_with_quarteryear(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
        self.fields['quarter_job'].widget = forms.Select(choices =[('','Select Quarter'),
                                                        ('First_Quarter','first Quarter(Jul-Sep)'),
                                                        ('Second_Quarter','Second Quarter(Oct-Dec)'),
                                                        ('Third_Quarter','Third Quarter(Jan-Mrrch)'),
                                                        ('Fourth_Quarter','Fourth Quarter(Apr-June)')],
                                                    attrs={'class':'form-control form-control-uniform','disabled':'true',})
    class Meta:
        model=JobOpportunities
        fields = ('year_job','quarter_job','job_type','female','male')
        widgets = {
            'job_type':forms.Select(attrs={'class':'form-control form-control-uniform','disabled':'true'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class EducationStatusForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(EducationStatusForm,self).__init__(*args,**kwargs)
        self.fields['year_edu'].widget = forms.Select(choices = return_year_with_quarteryear(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
        self.fields['quarter_edu'].widget = forms.Select(choices =[('','Select Quarter'),
                                                        ('First_Quarter','first Quarter(Jul-Sep)'),
                                                        ('Second_Quarter','Second Quarter(Oct-Dec)'),
                                                        ('Third_Quarter','Third Quarter(Jan-Mrrch)'),
                                                        ('Fourth_Quarter','Fourth Quarter(Apr-June)')],
                                                    attrs={'class':'form-control form-control-uniform','disabled':'true',})
    class Meta:
        model=EducationalStatus
        fields = ('year_edu','quarter_edu','education_type','female','male')
        widgets = {
            'education_type':forms.Select(attrs={'class':'form-control form-control-uniform','disabled':'true'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class FemalesInPositionForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(FemalesInPositionForm,self).__init__(*args,**kwargs)
        self.fields['year_fem'].widget = forms.Select(choices = return_year_with_quarteryear(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
        self.fields['quarter_fem'].widget = forms.Select(choices =[('','Select Quarter'),
                                                        ('First_Quarter','first Quarter(Jul-Sep)'),
                                                        ('Second_Quarter','Second Quarter(Oct-Dec)'),
                                                        ('Third_Quarter','Third Quarter(Jan-Mrrch)'),
                                                        ('Fourth_Quarter','Fourth Quarter(Apr-June)')],
                                                    attrs={'class':'form-control form-control-uniform','disabled':'true',})
    class Meta:
        model=FemalesInPosition
        fields = ('year_fem','quarter_fem','high_position','med_position','high_position_male','med_position_male')
        widgets = {
            'high_position':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_high_position")'}),
            'med_position':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_med_position")'}),
            'high_position_male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_high_position_male")'}),
            'med_position_male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_med_position_male")'}),
        }

# Project Employees Form
class EmployeesFormProject(forms.ModelForm):
    class Meta:
        model=Employees
        fields = ('employment_type','female','male')
        widgets = {
            'employment_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class JobCreatedFormProject(forms.ModelForm):
    class Meta:
        model=JobOpportunities
        fields = ('job_type','female','male')
        widgets = {
            'job_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }

class EducationStatusFormProject(forms.ModelForm):    
    class Meta:
        model=EducationalStatus
        fields = ('education_type','female','male')
        widgets = {
            'education_type':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'male':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_male")'}),
            'female':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_female")'}),
        }



class MarketDestinationForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(MarketDestinationForm,self).__init__(*args,**kwargs)
        self.fields['year_destn'].widget = forms.Select(choices = return_years(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
    class Meta:
        model=MarketDestination
        fields = ('domestic','export','year_destn')
        widgets = {
            'domestic':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_domestic")'}),
            'export':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_export")'}),
        }

class MarketTargetForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(MarketTargetForm,self).__init__(*args,**kwargs)
        self.fields['year_target'].widget = forms.Select(choices = return_years(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
    class Meta:
        model=MarketTarget
        fields = ('further_proc_power','final_consumer','restaurant_and_hotels',
                    'institutions','epsa','hospitals','agents','wholesaler_distributor',
                    'retailer','other','year_target')
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
    
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(SourceAmountIputsForm,self).__init__(*args,**kwargs)
        self.fields['year_src'].widget = forms.Select(choices = return_years(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})
    class Meta:
        model=SourceAmountIputs
        fields = ('import_company','govt_suplied','purchase_from_farmer','purchase_from_union',
                    'purchase_from_agents','purchase_from_other','year_src')
        widgets = {
            'import_company':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_import_company")'}),
            'govt_suplied':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_govt_suplied")'}),
            'purchase_from_farmer':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_farmer")'}),
            'purchase_from_union':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_union")'}),
            'purchase_from_agents':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_agents")'}),
            'purchase_from_other':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_purchase_from_other")'}),
        }

class PowerConsumptionForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.company = kwargs.pop('company')
        super(PowerConsumptionForm,self).__init__(*args,**kwargs)
        self.fields['year_pc'].widget = forms.Select(choices = return_years(self.company),
                                                    attrs={'class':'form-control form-control-uniform'})

    class Meta:
        model=PowerConsumption
        fields = ('year_pc','installed_capacity','current_supply')
        widgets = {
            'installed_capacity':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_installed_capacity")'}),
            'current_supply':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_current_supply")'}),
        }

class InistituteForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    class Meta:
        model = Company
        fields = (
            'name','name_am','logo','detail','detail_am'
        )
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name Of the Inistitute'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Name Of the Inistitute'}),
            'logo':forms.FileInput(attrs={'class':'form-control'}),
            'detail':forms.Textarea(attrs={'class':'summernote'}),
            'detail_am':forms.Textarea(attrs={'class':'summernote'}),
        }


class MyCompanyDetailForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.main_type = kwargs.pop('main_type')
        super(MyCompanyDetailForm,self).__init__(*args,**kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=self.main_type)
        self.fields['working_hours'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Working hours")
        self.fields['working_hours'].empty_label = "Select Working Hour"
        self.fields['certification'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Certifications")
        self.fields['management_tools'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Management Tools")
        self.fields['source_of_energy'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Source of Energy")
        self.fields['support_required'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Areas of Major Challenges")
        self.fields['lab_test_analysis'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Laboratory Test Analysis")
        self.fields['lab_equipment'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Laboratory Equipment")

    class Meta:
        model=Company
        fields=(
            'expansion_plan','category','working_hours','certification',
            'orgn_strct','lab_test_analysis','lab_equipment',
            'outsourced_test_param',
            'conducted_research','new_product_developed',
            'electric_power','water_supply','telecom','marketing_department','support_required',
            'e_commerce','active_database','waste_trtmnt_system',
            'efluent_treatment_plant','env_mgmt_plan','management_tools','source_of_energy',
            'gas_carb_emision','compound_allot','comunity_compliant', 
            'env_focal_person','safety_profesional','notification_procedure', 
            'university_linkage','recall_system',
            'quality_defects','gas_waste_mgmnt_measure',
            
            )
        widgets = {
                'expansion_plan':forms.Textarea(attrs={'class':'summernote'}),
                'category':forms.SelectMultiple(attrs={'class':'form-control'}),
                'orgn_strct':forms.FileInput(),
                'lab_test_analysis':forms.SelectMultiple(attrs={'class':'form-control'}),
                'lab_equipment':forms.SelectMultiple(attrs={'class':'form-control'}),
                'outsourced_test_param':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision':forms.Textarea(attrs={'class':'summernote'}),
                'comunity_compliant':forms.Textarea(attrs={'class':'summernote'}), 
                'university_linkage':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure':forms.Textarea(attrs={'class':'summernote'}),
                'working_hours':forms.Select(attrs={'class':'form-control form-control-uniform'}),
                'certification':forms.SelectMultiple(attrs={'class':'form-control'}),
                'management_tools':forms.SelectMultiple(attrs={'class':'form-control'}),
                'source_of_energy':forms.SelectMultiple(attrs={'class':'form-control'}),
                'support_required':forms.SelectMultiple(attrs={'class':'form-control'}),
            }


class CompanyAddressForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CompanyAddressForm,self).__init__(*args,**kwargs)
        self.fields['region'].empty_label = "Select Region"

    class Meta:
        model=CompanyAddress
        fields = ('region','city_town','subcity_zone','woreda','kebele','local_area',
                    'phone_number','fax','email','website','facebooklink','twiterlink','instagramlink',
                    'linkedinlink','googlelink')
        
        widgets = {
            'region':forms.Select(attrs={'class':'form-control'}),
            'city_town':forms.TextInput(attrs={'class':'form-control','placeholder':'City/Town'}),
            'subcity_zone':forms.TextInput(attrs={'class':'form-control','placeholder':'Subcity/Zone'}),
            'woreda':forms.TextInput(attrs={'class':'form-control','placeholder':'Woreda'}),
            'kebele':forms.TextInput(attrs={'class':'form-control','placeholder':'Kebele'}),
            'local_area':forms.TextInput(attrs={'class':'form-control','placeholder':'Local Area'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number', "data-mask": "+251-99999-9999"}),
            'fax':forms.TextInput(attrs={'class':'form-control','placeholder':'Fax'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}),
            'website':forms.TextInput(attrs={'class':'form-control','placeholder':'Website Link'}),
            'facebooklink':forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook Account Link'}),
            'twiterlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Twitter Account Link'}),
            'instagramlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram Link'}),
            'linkedinlink':forms.TextInput(attrs={'class':'form-control','placeholder':'Linkedin Link'}),
            'googlelink':forms.TextInput(attrs={'class':'form-control','placeholder':'Google Account Link'}),
        }

class CompanyProfileForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    
    def __init__(self,*args,**kwargs):
        super(CompanyProfileForm,self).__init__(*args,**kwargs)
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['ownership_form'].empty_label="Select Form Of Ownership"

    class Meta:
        model = Company
        fields = (
            'ownership_form','name','name_am','geo_location','logo','established_yr',
            'main_category','trade_license','detail','detail_am',
            )
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in English'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in Amharic'}),
            'logo':forms.FileInput(attrs={'class':''}),
            'geo_location':gis_form.OSMWidget(attrs={'required':True,'map_width': 800, 'map_height': 400}),
            'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
            'main_category':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            'trade_license':forms.FileInput(attrs={'class':''}),
            'ownership_form':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            'detail':forms.Textarea(attrs={'class':'summernote'}),
            'detail_am':forms.Textarea(attrs={'class':'summernote'}),
        }
 

class CompanyProfileForm_Superadmin(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        super(CompanyProfileForm_Superadmin,self).__init__(*args,**kwargs)
        self.fields['contact_person'].queryset = UserProfile.objects.filter(is_company_admin=True).exclude(
                                                Exists(Company.objects.filter(contact_person=OuterRef('pk'))))
        self.fields['contact_person'].empty_label="Select Company contact Person"
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['ownership_form'].empty_label="Select Form Of Ownership"

    class Meta:
        model = Company
        fields = (
            'contact_person','name','name_am','logo','ownership_form','established_yr',
            'main_category','trade_license','geo_location','detail','detail_am',
            )
        widgets = {
            'contact_person':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in English'}),
            'name_am':forms.TextInput(attrs={'class':'form-control','placeholder':'Company Name in Amharic'}),
            'logo':forms.FileInput(attrs={'class':''}),
            'geo_location':gis_form.OSMWidget(attrs={'map_width': 900, 'map_height': 400}),
            # 'geo_location':GooglePointFieldWidget,
            'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
            'main_category':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            'trade_license':forms.FileInput(attrs={'class':''}),
            'ownership_form':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'detail':forms.Textarea(attrs={'class':'summernote'}),
            'detail_am':forms.Textarea(attrs={'class':'summernote'}),
        }

     

class CompanyRatingForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CompanyRatingForm,self).__init__(*args,**kwargs)
        self.fields['company_condition'].empty_label="Select One Status"
        self.fields['company_condition'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Industry Status Checklists")

    class Meta:
        model = Company
        fields = ('company_condition',)
        widgets = {
            'company_condition':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }

class CompanyUpdateForm(forms.ModelForm):
    #  default_lat=38.781596,default_lon=8.983564,
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def __init__(self,*args,**kwargs):
        self.main_type = kwargs.pop('main_type')
        self.company = kwargs.pop("company")
        super(CompanyUpdateForm,self).__init__(*args,**kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=self.main_type)
        self.fields['certification'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Certifications")
        self.fields['source_of_energy'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Source of Energy")
        self.fields['support_required'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Areas of Major Challenges")
        self.fields['management_tools'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Management Tools")
        self.fields['working_hours'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Working hours")
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['lab_test_analysis'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Laboratory Test Analysis")
        self.fields['lab_equipment'].queryset = CompanyDropdownsMaster.objects.filter(chk_type="Laboratory Equipment")
        self.fields['contact_person'].queryset =  UserProfile.objects.filter(is_company_admin=True,contact_person__id=self.company.id)

    class Meta:
        model=Company
        fields=('name','contact_person','name_am','logo','established_yr','category','ownership_form','trade_license',
            'expansion_plan','geo_location','detail','detail_am',
            'orgn_strct','certification','management_tools','working_hours',
            'lab_test_analysis','lab_equipment','outsourced_test_param',
            'conducted_research','new_product_developed',
            'electric_power','water_supply','telecom','marketing_department','source_of_energy',
            'e_commerce','active_database','waste_trtmnt_system',
            'efluent_treatment_plant','env_mgmt_plan',
            'gas_carb_emision','compound_allot','comunity_compliant','env_focal_person','safety_profesional',
            'notification_procedure','university_linkage','recall_system',
            'quality_defects','gas_waste_mgmnt_measure','support_required',
            
            )
        widgets = {
                # 'contact_person':forms.TextInput(attrs={'class':'form-control'}),
                'expansion_plan':forms.Textarea(attrs={'class':'summernote'}),
                'orgn_strct':forms.FileInput(),
                'geo_location':gis_form.OSMWidget(attrs={'map_width': 500, 'map_height': 250}),
                # 'geo_location':GooglePointFieldWidget,
                'lab_test_analysis':forms.SelectMultiple(attrs={'class':'form-control'}),
                'lab_equipment':forms.SelectMultiple(attrs={'class':'form-control'}),
                'outsourced_test_param':forms.Textarea(attrs={'class':'summernote'}),
                'conducted_research':forms.Textarea(attrs={'class':'summernote'}),
                'new_product_developed':forms.Textarea(attrs={'class':'summernote'}),
                'waste_trtmnt_system':forms.Textarea(attrs={'class':'summernote'}),
                'gas_carb_emision':forms.Textarea(attrs={'class':'summernote'}),
                'comunity_compliant':forms.Textarea(attrs={'class':'summernote'}), 
                'university_linkage':forms.Textarea(attrs={'class':'summernote'}),
                'quality_defects':forms.Textarea(attrs={'class':'summernote'}),
                'gas_waste_mgmnt_measure':forms.Textarea(attrs={'class':'summernote'}),
                'detail':forms.Textarea(attrs={'class':'summernote'}),
                'detail_am':forms.Textarea(attrs={'class':'summernote'}),
                'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
            }
        
     

class CompanyMessageForm(forms.ModelForm):
    class Meta:
        model = CompanyMessage
        fields = ('name', 'email', 'message')


class ProjectProductForm(forms.ModelForm):
    class Meta:
        model=ProjectProductQuantity
        fields = (
            'product_tobe_produced','expected_normal_capacity','expected_anual_sales',
            'local_share','export_share',
        )
        widgets = {
            'product_tobe_produced':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product To be Produced'}),
            'expected_normal_capacity':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_expected_normal_capacity")'}),
            'expected_anual_sales':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_expected_anual_sales")'}),
            'local_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_local_share")'}),
            'export_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_export_share")'}),
        }


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model=ProjectState
        fields = (
            'percentage_construction_performance','machinery_purchase_performance','factory_building_performance',
            'machinery_installation','commissioning_work','rawmaterial_preparation','hremployment_training',
            'testproduct','certification',
        )
        widgets = {
            'percentage_construction_performance':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Costruction Performance', 'onkeyup': 'isNumber("id_percentage_construction_performance")'}),
            'machinery_purchase_performance':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Machinery Purchase Performance', 'onkeyup': 'isNumber("id_machinery_purchase_performance")'}),
            'factory_building_performance':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Factory Building Performance', 'onkeyup': 'isNumber("id_factory_building_performance")'}),
            'machinery_installation':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Machinery Installation', 'onkeyup': 'isNumber("id_machinery_installation")'}),
            'commissioning_work':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Commissioning Work','onkeyup': 'isNumber("id_commissioning_work")'}),
            'rawmaterial_preparation':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Raw Material Operation' ,'onkeyup': 'isNumber("id_rawmaterial_preparation")'}),
            'hremployment_training':forms.TextInput(
                attrs={'class': 'form-control', 'placeholder':'HR Employment Training','onkeyup': 'isNumber("id_hremployment_training")'}),
            'testproduct':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Test Product', 'onkeyup': 'isNumber("id_testproduct")'}),
            'certification':forms.TextInput(
                attrs={'class': 'form-control','placeholder':'Certification', 'onkeyup': 'isNumber("id_certification")'}),
        }

class LandUsageForm(forms.ModelForm):
    class Meta:
        model=LandUsage
        fields = (
            'total_land_size','production_building','office_building','warehouse','other',
        )
        widgets = {
            'total_land_size':forms.TextInput(attrs={'class': 'form-control','placeholder':'Total Land Size', 'onkeyup': 'isNumber("id_total_land_size")'}),
            'production_building':forms.TextInput(attrs={'class': 'form-control','placeholder':'Production Building', 'onkeyup': 'isNumber("id_production_building")'}),
            'office_building':forms.TextInput(attrs={'class': 'form-control','placeholder':'Office Building', 'onkeyup': 'isNumber("id_office_building")'}),
            'warehouse':forms.TextInput(attrs={'class': 'form-control','placeholder':'Warehouse', 'onkeyup': 'isNumber("id_warehouse")'}),
            'other':forms.TextInput(attrs={'class': 'form-control','placeholder':'Others', 'onkeyup': 'isNumber("id_other")'}),
        }




class InvestmentProjectForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    def __init__(self,*args,**kwargs):
        self.contact_person = kwargs.pop('contact_person')
        super(InvestmentProjectForm,self).__init__(*args,**kwargs)
        self.fields['contact_person'].empty_label = "Select Project Contact Person"
        self.fields['contact_person'].queryset = self.contact_person
        self.fields['project_classification'].empty_label = "Select Project Classification"
        self.fields['project_classification'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Project Classification")
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['ownership_form'].empty_label = "Select Form of Ownership"

    class Meta:
        model=InvestmentProject
        fields = ('project_name','project_name_am','image','ownership_form','established_yr','owners_nationality','geo_location','owner_share','bank_share','capital_in_dollary',
            'investment_license','issued_date','sector','project_classification',
            'contact_person','description','description_am',
            )
        widgets = {
            'image':forms.FileInput(attrs={}),
            'ownership_form':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            'project_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in English'}),
            'owners_nationality':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owners Nationality'}),
            'project_name_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in Amharic'}),
            'owner_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_owner_share")'}),
            'bank_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_bank_share")'}),
            'capital_in_dollary':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_in_dollary")'}),
            'investment_license':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment License Code'}),
            'issued_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'sector':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'project_classification':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'contact_person':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
            'geo_location':gis_form.OSMWidget(attrs={'map_width': 800, 'map_height': 400}),
            # 'geo_location':GooglePointFieldWidget,
            'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
        }

class InvestmentProjectForm_ForSuperAdmin(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    def __init__(self,*args,**kwargs):
        super(InvestmentProjectForm_ForSuperAdmin,self).__init__(*args,**kwargs)
        self.fields['company'].empty_label = "Select A Company"
        self.fields['company'].queryset = Company.objects.all()
        self.fields['project_classification'].empty_label = "Select Project Classification"
        self.fields['project_classification'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Project Classification")
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['ownership_form'].empty_label = "Select Form of Ownership"
        
    class Meta:
        model=InvestmentProject
        fields = ('company','project_name','project_name_am','image','ownership_form','established_yr','owners_nationality','geo_location','owner_share','bank_share','capital_in_dollary',
            'investment_license','issued_date','sector','project_classification',
            'description','description_am',
            )
        widgets = {
            'company':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'image':forms.FileInput(),
            'ownership_form':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            'geo_location':gis_form.OSMWidget(attrs={'map_width': 800, 'map_height': 400}),
            # 'geo_location':GooglePointFieldWidget,
            'owners_nationality':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owners Nationality'}),
            'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
            'project_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in English'}),
            'project_name_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in Amharic'}),
            'owner_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_owner_share")'}),
            'bank_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_bank_share")'}),
            'capital_in_dollary':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_in_dollar")'}),
            'investment_license':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment License Code'}),
            'issued_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'sector':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'project_classification':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'description_am':forms.Textarea(attrs={'class':'summernote'}),
        }



class InvestmentProjectDetailForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.sector = kwargs.pop("sector")
        super(InvestmentProjectDetailForm,self).__init__(*args,**kwargs)
        self.fields['product_type'].queryset = Category.objects.filter(category_type=self.sector)
        self.fields['technology'].empty_label = "Select Technology to be Used"
        self.fields['technology'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Technology")
        self.fields['land_acquisition'].empty_label = "Select Land Acquisition"
        self.fields['land_acquisition'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Land Acquisition")
        self.fields['automation'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Automation")
        self.fields['automation'].empty_label = "Select Automation"
        self.fields['automation'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Automation")
        self.fields['mode_of_project'].empty_label = "Select Mode of Project"
        self.fields['mode_of_project'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Mode Of Project")
        self.fields['facility_design'].empty_label = "Select Facility Design"
        self.fields['facility_design'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Facility Design")

    class Meta:
        model = InvestmentProject
        fields = (
            'product_type','site_location_name','land_acquisition',
            'distance_f_strt','remaining_work',
            'major_problems','operational_time','annual_raw_material',
            'power_need','water_suply','cond_provided_for_wy',
            'target_market','env_impac_ass_doc','capital_utilization',
            'technology','automation','mode_of_project','facility_design',
        )
        widgets = {
            'land_acquisition':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'product_type':forms.SelectMultiple(attrs={'class':'form-control form-control-uniform'}),
            'site_location_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Location Name'}),
            'distance_f_strt':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_distance_f_strt")'}),
            'remaining_work':forms.Textarea(attrs={'class':'summernote'}),
            'major_problems':forms.Textarea(attrs={'class':'summernote'}),
            'operational_time':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'annual_raw_material':forms.Textarea(attrs={'class':'summernote'}),
            'power_need':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_power_need")'}),
            'water_suply':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_water_suply")'}),
            'cond_provided_for_wy':forms.Textarea(attrs={'class':'summernote'}),
            'target_market':forms.Textarea(attrs={'class':'summernote'}),
            'env_impac_ass_doc':forms.FileInput(attrs={'class':'form-control'}),
            'capital_utilization':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_utilization")'}),
            'technology':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'automation':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'mode_of_project':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'facility_design':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }

class InvestmentProjectDetailForm_Admin(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.sector = kwargs.pop("sector")
        self.contact_person = kwargs.pop("contact_person")
        super(InvestmentProjectDetailForm_Admin,self).__init__(*args,**kwargs)
        self.fields['product_type'].queryset = Category.objects.filter(category_type=self.sector)
        self.fields['technology'].empty_label = "Select Technology to be Used"
        self.fields['technology'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Technology")
        self.fields['automation'].empty_label = "Select Automation"
        self.fields['automation'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Automation")
        self.fields['mode_of_project'].empty_label = "Select Mode of Project"
        self.fields['mode_of_project'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Mode Of Project")
        self.fields['facility_design'].empty_label = "Select Facility Design"
        self.fields['facility_design'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Facility Design")
        self.fields['contact_person'].empty_label = "Select A Contact Person"
        self.fields['contact_person'].queryset= self.contact_person
        self.fields['land_acquisition'].empty_label = "Select Land Acquisition"
        self.fields['land_acquisition'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Land Acquisition")

    class Meta:
        model = InvestmentProject
        fields = (
            'product_type','site_location_name','contact_person','land_acquisition',
            'distance_f_strt','remaining_work',
            'major_problems','operational_time','annual_raw_material',
            'power_need','water_suply','cond_provided_for_wy',
            'target_market','env_impac_ass_doc','capital_utilization',
            'technology','automation','mode_of_project','facility_design',
        )
        widgets = {
            'land_acquisition':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'product_type':forms.SelectMultiple(attrs={'class':'form-control form-control-uniform'}),
            'site_location_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Location Name'}),
            'distance_f_strt':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_distance_f_strt")'}),
            'remaining_work':forms.Textarea(attrs={'class':'summernote'}),
            'major_problems':forms.Textarea(attrs={'class':'summernote'}),
            'operational_time':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'annual_raw_material':forms.Textarea(attrs={'class':'summernote'}),
            'power_need':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_power_need")'}),
            'water_suply':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_water_suply")'}),
            'cond_provided_for_wy':forms.Textarea(attrs={'class':'summernote'}),
            'target_market':forms.Textarea(attrs={'class':'summernote'}),
            'env_impac_ass_doc':forms.FileInput(attrs={'class':'form-control'}),
            'capital_utilization':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_utilization")'}),
            'technology':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'automation':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'mode_of_project':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'facility_design':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'contact_person':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }


class ProjectUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)
    def __init__(self,*args,**kwargs):
        self.sector = kwargs.pop("sector")
        self.contact_person = kwargs.pop('contact_person')
        super(ProjectUpdateForm,self).__init__(*args,**kwargs)
        self.fields['product_type'].queryset = Category.objects.filter(category_type=self.sector)
        self.fields['ownership_form'].queryset = CompanyDropdownsMaster.objects.filter(chk_type='Forms of Ownership')
        self.fields['ownership_form'].empty_label = "Select Ownership Form"
        self.fields['technology'].empty_label = "Select Technology to be Used"
        self.fields['technology'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Technology")
        self.fields['automation'].empty_label = "Select Automation"
        self.fields['automation'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Automation")
        self.fields['mode_of_project'].empty_label = "Select Mode of Project"
        self.fields['mode_of_project'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Mode Of Project")
        self.fields['facility_design'].empty_label = "Select Facility Design"
        self.fields['facility_design'].queryset= ProjectDropDownsMaster.objects.filter(dropdown_type="Facility Design")
        self.fields['contact_person'].empty_label = "Select A Contact Person"
        self.fields['contact_person'].queryset= self.contact_person
        self.fields['project_classification'].empty_label = "Select Project Classification"
        self.fields['project_classification'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Project Classification")
        self.fields['land_acquisition'].empty_label = "Select Land Acquisition"
        self.fields['land_acquisition'].queryset = ProjectDropDownsMaster.objects.filter(dropdown_type="Land Acquisition")

    class Meta:
        model = InvestmentProject
        fields = ('project_name','project_name_am','image','ownership_form','established_yr','geo_location','owner_share','bank_share','capital_in_dollary',
            'investment_license','issued_date','sector','project_classification',
            'contact_person','description','description_am','product_type','site_location_name',
            'distance_f_strt','remaining_work','land_acquisition',
            'major_problems','operational_time','annual_raw_material',
            'power_need','water_suply','cond_provided_for_wy',
            'target_market','env_impac_ass_doc','capital_utilization',
            'technology','automation','mode_of_project','facility_design',
        )
        widgets = {
            'land_acquisition':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'image':forms.FileInput(),
            'ownership_form':forms.Select(attrs={'class':'form-control form-control-uniform',}),
            # 'geo_location':gis_form.OSMWidget(attrs={'map_width': 600, 'map_height': 400}),
            'geo_location':GooglePointFieldWidget,
            'established_yr':forms.TextInput(attrs={'class':'form-control','onkeyup':'isNumber("id_established_yr")','placeholder':'Established Year (E.C)','maxlength':'4'}),
            'project_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in English'}),
            'project_name_am':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment Project Name in Amharic'}),
            'owner_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_owner_share")'}),
            'bank_share':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_bank_share")'}),
            'capital_in_dollary':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_in_dollary")'}),
            'investment_license':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Investment License Code'}),
            'issued_date':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'sector':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'project_classification':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'contact_person':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'description':forms.Textarea(attrs={'class':'summernote'}),
            'product_type':forms.SelectMultiple(attrs={'class':'form-control form-control-uniform'}),
            'site_location_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Site Location Name'}),
            'distance_f_strt':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_distance_f_strt")'}),
            'remaining_work':forms.Textarea(attrs={'class':'summernote'}),
            'major_problems':forms.Textarea(attrs={'class':'summernote'}),
            'operational_time':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'annual_raw_material':forms.Textarea(attrs={'class':'summernote'}),
            'power_need':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_power_need")'}),
            'water_suply':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_water_suply")'}),
            'cond_provided_for_wy':forms.Textarea(attrs={'class':'summernote'}),
            'target_market':forms.Textarea(attrs={'class':'summernote'}),
            'env_impac_ass_doc':forms.FileInput(attrs={'class':'form-control'}),
            'capital_utilization':forms.TextInput(attrs={'class': 'form-control', 'onkeyup': 'isNumber("id_capital_utilization")'}),
            'technology':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'automation':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'mode_of_project':forms.Select(attrs={'class':'form-control form-control-uniform'}),
            'facility_design':forms.Select(attrs={'class':'form-control form-control-uniform'}),
        }
        

class SliderImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model = HomePageSlider
        fields = ('slider_image','alt_text')
        widgets = {
            'slider_image':forms.FileInput(attrs={'class':'form-control'}),
            'alt_text':forms.TextInput(attrs={'class':'form-control','placeholder':'Image Alt Text'})
        }