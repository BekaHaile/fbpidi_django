
from admin_site.models import (Category, CompanyDropdownsMaster,
                               ProjectDropDownsMaster,RegionMaster)
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

allowed_file_extensions = ['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls']
allowed_image_extensions = ['png','jpg',]

CAT_LIST = (
    ('','Select Company Type'),
    ("Food",'Food'),
    ("Beverage",'Beverages'),
    ("Pharmaceuticals",'Pharmaceuticals'),
)

		


class Company(models.Model):
	main_category = models.CharField(max_length=100,verbose_name="Company Type",choices=CAT_LIST)
	name = models.CharField(verbose_name="Company Name in English", max_length=255,null=True)
	name_am = models.CharField(verbose_name="Company Name in Amharic", max_length=255,null=True)
	logo = models.FileField(max_length=254, verbose_name="Logo of the company",
							help_text="png,jpg Max size 10MB", null=True,
							upload_to="company/logo/",
							validators=[FileExtensionValidator(allowed_extensions=allowed_image_extensions)])
	geo_location	= gis_models.PointField(verbose_name="Company Location",null=True)
	ownership_form = models.ForeignKey(CompanyDropdownsMaster,on_delete=models.RESTRICT,null=True,
										verbose_name="Form Of Ownership",related_name="ownership_form")
	established_yr	= models.IntegerField(verbose_name="Established Year",default=0)
	detail = models.TextField(verbose_name="Company Description in English",default="")
	detail_am = models.TextField(verbose_name="Company Description in Amharic",default="")
	contact_person	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,related_name="contact_person") # contact person
	category	= models.ManyToManyField(Category,related_name="company_category",verbose_name="Company Product Types") # category
	expansion_plan	= models.TextField(verbose_name="Expansion Plan in English", null = True)
	expansion_plan_am	= models.TextField(verbose_name="Expansion Plan in Amharic", null = True)
	trade_license	= models.FileField(max_length=254, verbose_name="your Trade License",
									help_text="Images and pdf files less than 10MB", null=True,
									upload_to="company/trade_license/",
									validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)])
	working_hours	= models.ForeignKey(CompanyDropdownsMaster,on_delete=models.RESTRICT,related_name="working_hours",null=True)
	orgn_strct	= models.FileField(max_length=254, verbose_name="Organizational Structure",
							help_text="Image and pdf files less thatn 10MB", null=True,blank=True,
							upload_to="company/organization_structure/",
							validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)])
	lab_test_analysis = models.ManyToManyField(CompanyDropdownsMaster,verbose_name="Laboratory test analysis in english",blank=True,related_name="lab_test_analysis") 
	lab_equipment	= models.ManyToManyField(CompanyDropdownsMaster,verbose_name="Laboratory equipment",related_name="lab_equipment",blank=True) 
	outsourced_test_param = models.TextField(verbose_name="Outsourced test parameters and contract agreements in english",null=True,blank=True)
	outsourced_test_param_am = models.TextField(verbose_name="Outsourced test parameters and contract agreements in amharic", null=True,blank=True)
	certification	= models.ManyToManyField(CompanyDropdownsMaster,related_name="certification",verbose_name="Which certificate have you received?")  
	conducted_research	= models.TextField(verbose_name="Conducted research and development",null=True,blank=True)
	conducted_research_am	= models.TextField(verbose_name="Conducted research and development in amharic",null=True,blank=True)
	new_product_developed	= models.TextField(verbose_name="New Product_Developed",null=True,blank=True)
	new_product_developed_am	= models.TextField(verbose_name="New Product_Developed Amharic",null=True,blank=True) # under question
	management_tools = models.ManyToManyField(CompanyDropdownsMaster,verbose_name="Management Tools",related_name="mgmt_tools")
	electric_power = models.BooleanField(default=False)
	water_supply = models.BooleanField(default=False)
	telecom	= models.BooleanField(default=False)
	marketing_department = models.BooleanField(default=False,verbose_name="Does the company have Marketing Department section?")
	e_commerce	= models.BooleanField(default=False,verbose_name="Do you use E-Commerce?")
	active_database =	models.BooleanField(default=False,verbose_name="Do you adopt any active data base system?")
	waste_trtmnt_system	= models.TextField(verbose_name="Waste Treatment and disposal system in english",null=True,blank=True)
	waste_trtmnt_system_am	= models.TextField(verbose_name="Waste Treatment and disposal system in amharic",null=True,blank=True)
	efluent_treatment_plant = models.BooleanField(default=False,verbose_name="Do you have effluent treatment plant?")
	env_mgmt_plan = models.BooleanField(default=False,verbose_name="Does the company have Environmental management plan?")
	source_of_energy = models.ManyToManyField(CompanyDropdownsMaster,related_name="source_of_energy",blank=True)
	gas_carb_emision = models.TextField(verbose_name="Measure of Gas/carbon emission to the environment in english",null=True,blank=True)
	gas_carb_emision_am = models.TextField(verbose_name="Measure of Gas/carbon emission to the environment in amharic",null=True,blank=True)
	compound_allot	= models.BooleanField(default=False,verbose_name="Does the company allot 5%\ of the compound for greenery?")
	comunity_compliant	= models.TextField(verbose_name="Environmental issue compliant with the community in english",null=True,blank=True)
	comunity_compliant_am	= models.TextField(verbose_name="Environmental issue compliant with the community in amharic",null=True,blank=True)
	env_focal_person = models.BooleanField(default=False,verbose_name="Does the company have Environmental and social focal person?")
	safety_profesional	 = models.BooleanField(default=False,verbose_name="Does the company have safety professionals?")
	notification_procedure	= models.BooleanField(default=False,verbose_name="Do you have proper notification procedure to inform EFDA regarding proper disposal?")
	university_linkage	= models.TextField(verbose_name="Industry University linkage in english",null=True,blank=True)
	university_linkage_am	= models.TextField(verbose_name="Industry University linkage in amharic",null=True,blank=True)
	recall_system	= models.BooleanField(default=False,verbose_name="Is there a Recall system due to quality issue?")
	quality_defects_am	= models.TextField(verbose_name="What quality defect frequently observed in your product? in amharic",null=True,blank=True)
	quality_defects	= models.TextField(verbose_name="What quality defect frequently observed in your product? in English",null=True,blank=True)
	gas_waste_mgmnt_measure	= models.TextField(verbose_name="What measures does your company introduced to reduce its gas and waste management? in English",null=True,blank=True)
	gas_waste_mgmnt_measure_am	= models.TextField(verbose_name="What measures does your company introduced to reduce its gas and waste management? in amharic",null=True,blank=True)
	support_required	= models.ManyToManyField(CompanyDropdownsMaster,verbose_name="What kind of support do you need to increase your production and market",related_name="major_challenges")
	company_condition = models.ForeignKey(CompanyDropdownsMaster,on_delete=models.RESTRICT,null=True,verbose_name="Status of processing/ industry facility",related_name="company_status")
	is_active = models.BooleanField(default=False)
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='company_created_by',null=True)
	created_date	= models.DateTimeField(auto_now_add=True)
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='company_updated_by',null=True)
	last_updated_date	= models.DateTimeField(null=True)
	expired	= models.BooleanField(default=False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('-created_date',)

	def get_company_address(self):
		try:
			return CompanyAddress.objects.get(company=self)
		except Exception as e:
			return None

	# These 2 methods r used for Company serialization
	def get_company_certificates(self): 
		return Certificates.objects.filter(company =self)

	def get_company_category(self):
		return self.category.all()

	# I will delete these three methods once I have finished the main tasks and used the get_company_address for all templates
	def get_image(self):
		return self.logo.url
	
	def phone_number(self):
		address = self.get_company_address()
		return address.phone_number if address else ''
	
	def location(self):
		address = self.get_company_address()
		return f"{address.city_town}" if address else ''
	

# Company Address Model
class CompanyAddress(models.Model):
	company = models.OneToOneField(Company,on_delete=models.CASCADE,related_name="company_address")
	region = models.ForeignKey(RegionMaster, verbose_name="Rigion",on_delete=models.RESTRICT)
	city_town = models.CharField(max_length=255, verbose_name="City Town")
	subcity_zone = models.CharField(max_length=255, verbose_name="Subcity zone")
	woreda = models.CharField(max_length=255, verbose_name="Woreda")
	kebele = models.CharField(max_length=255, verbose_name="Kebele",null=True,blank=True)
	local_area = models.CharField(max_length=255, verbose_name="Local Area",null=True,blank=True)
	phone_number = models.CharField(max_length=255, verbose_name="Phone Number")
	fax = models.CharField(max_length=255, verbose_name="Fax",null=True,blank=True)
	email = models.EmailField(verbose_name="Email Link", max_length=255,null=True,blank=True)
	facebooklink = models.CharField(verbose_name="Facebook Link", max_length=255,null=True,blank=True)
	twiterlink = models.CharField(verbose_name="Twiter Link", max_length=255,null=True,blank=True)
	instagramlink = models.CharField(verbose_name="Instagram Link", max_length=255,null=True,blank=True)
	linkedinlink = models.CharField(verbose_name="Linkedin Link", max_length=255,null=True,blank=True)
	googlelink = models.CharField(verbose_name="Google Link", max_length=255,null=True,blank=True)
	timestamp = models.DateField(auto_now_add=True)


# Company current Investment capital based on the following attributes.
class InvestmentCapital(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="investment_capital")
	machinery_cost	= models.FloatField(default=0)
	building_cost	= models.FloatField(default=0)
	working_capital	= models.FloatField(default=0)
	timestamp = models.DateField(auto_now_add=True)

	def get_inv_cap(self):
		return float(self.machinery_cost+self.building_cost+self.working_capital)

# Certificates
class Certificates(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="certificates")
    name = models.CharField(max_length=100,null=True)
    certificate	= models.FileField(max_length=254,
									upload_to="company/certificates/",
                                    verbose_name="Certificate of Competency",
                                    help_text="Images and pdf files less thatn 10MB",
									validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)])
    timestamp = models.DateField(auto_now_add=True)

	

# Source and Amount of product input materials
class SourceAmountIputs(models.Model):		
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="source_amount_inputs",default=0)
	year =  models.IntegerField()
	import_company	= models.FloatField(default=0,verbose_name="Imported By Company",help_text="(Ton/Year)")
	govt_suplied	= models.FloatField(default=0,verbose_name="Government Supplied",help_text="(Ton/Year)")
	purchase_from_farmer	= models.FloatField(default=0,verbose_name="Direct purchase from Farmers",help_text="(Ton/Year)")
	purchase_from_union	= models.FloatField(default=0,verbose_name="Purchase from Cooperative unions",help_text="(Ton/Year)")
	purchase_from_agents	= models.FloatField(default=0,verbose_name="Purchase from Commission Agents",help_text="(Ton/Year)")
	purchase_from_other	= models.FloatField(default=0,verbose_name="Other Specify other",help_text="(Ton/Year)")
	timestamp = models.DateField(auto_now_add=True)

# Employees information/statistics
class Employees(models.Model):
	EMP_TYPE= [('','Select Employment Type'),
				('Permanent Employee','Permanent Employee'),
				('Temporary Employee','Temporary Employee'),
				('Foreign Employee','Foreign Employee')]
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="employees",null=True,blank=True)
	projct = models.ForeignKey('InvestmentProject',on_delete=models.CASCADE,related_name="project_employees",null=True,blank=True)
	year	= models.IntegerField(default=0,)
	employment_type	= models.CharField(max_length=200,verbose_name="The Employment Type", choices=EMP_TYPE)	
	male	= models.IntegerField(default=0,verbose_name="Number Of Male Employees")	
	female	= models.IntegerField(default=0,verbose_name="Number of Female Employees")	
	timestamp = models.DateField(auto_now_add=True)

# New Jobs Created Every Year
class JobOpportunities(models.Model):
	JOB_TYPE = [ ('','Select Job Type'),('Permanent','Permanent'),('Temporary','Temporary'),]
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="job_oportunities",null=True,blank=True)
	project = models.ForeignKey('InvestmentProject',on_delete=models.CASCADE,related_name="project_jobs",null=True,blank=True)
	year	= models.IntegerField(default=0)
	job_type = models.CharField(max_length=20,verbose_name="Types Of Job", choices=JOB_TYPE)
	male	= models.IntegerField(default=0)
	female	= models.IntegerField(default=0)	
	timestamp = models.DateField(auto_now_add=True)


# Employees Educational Status
class EducationalStatus(models.Model):
	EDUCATION_TYP = (('','Select Education Type'),('12th Graduate below','12th Graduate below'),('Deploma TVET','Deploma TVET'),('Degree','Degree'),('Masters','Masters'),('PhD','PhD'),)
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="educational_status",null=True,blank=True)
	project = models.ForeignKey('InvestmentProject',on_delete=models.CASCADE,related_name="project_edu_stat",null=True,blank=True)
	year = models.IntegerField()
	education_type	= models.CharField(verbose_name="Education Level ",choices=EDUCATION_TYP, max_length=2000)		
	male	= models.IntegerField(default=0)		
	female	= models.IntegerField(default=0)
	timestamp = models.DateField(auto_now_add=True)	

# Number of Female Employees in high positions
class FemalesInPosition(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="females_high_positions")
    year = models.IntegerField()
    high_position = models.IntegerField(default=0,verbose_name="High level position ",help_text="(CEO, Managerial positions)")
    med_position = models.IntegerField(default=0,verbose_name="Medium level position",help_text="(Department heads)")
    timestamp = models.DateField(auto_now_add=True)
    
# Yearly Marget Target In percent
class MarketTarget(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="market_target",default=0)
	year	= models.IntegerField(default=0,)
	further_proc_power 	= models.FloatField(verbose_name="Further processing factors ",default=0)	
	final_consumer	= models.FloatField(verbose_name="Final consumers ",default=0)	
	restaurant_and_hotels = models.FloatField(verbose_name="Restaurant and Hotels ",default=0)	
	institutions = models.FloatField(verbose_name="Institutions (University, military, cooperatives)",default=0)	
	epsa = models.FloatField(verbose_name="EPSA ",default=0)	
	hospitals	= models.FloatField(verbose_name="Hospitals ",default=0)	
	agents	= models.FloatField(verbose_name="Agents ",default=0)	
	wholesaler_distributor	= models.FloatField(verbose_name="Wholesaler/Distributor ",default=0)	
	retailer = models.FloatField(verbose_name="Retailer ",default=0)	
	other = models.FloatField(verbose_name="Others ",default=0)
	timestamp = models.DateField(auto_now_add=True)

# Yearly market destinations
class MarketDestination(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="market_destination",default=0)
	year	= models.IntegerField(default=0,)
	domestic = models.FloatField(verbose_name="Domestic %",default=0)	
	export	= models.FloatField(verbose_name="Export %",default=0)
	timestamp = models.DateField(auto_now_add=True)

# Daily Power consumption
class PowerConsumption(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="power_consumption",default=0)
	day	= models.DateField(verbose_name="Day",)
	installed_capacity = models.FloatField(verbose_name="Installed Capacity EP demand",help_text="kilowatt-hour (kWh) per day", default=0)	
	current_supply = models.FloatField(verbose_name="Currently Supplying EP",help_text="kilowatt-hour (kWh) per day", default=0)	
	timestamp = models.DateField(auto_now_add=True)



class CompanyStaff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, primary_key=True,related_name="company_staff")
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="staff_company")
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_company_name(self):
        return self.company.name if self.company.name else None

    def get_company(self):
        return Company.objects.get(user = self.user) if Company.objects.get(user = self.user) else None

class InvestmentProject(models.Model):
	company	= models.ForeignKey(Company, on_delete=models.CASCADE,related_name="company_project")
	image = models.ImageField(verbose_name="Project Image",blank=True,null=True)
	project_name = models.CharField(max_length=255,default="",verbose_name="Investment Company Name All Capital Letters")
	project_name_am = models.CharField(max_length=255,default="",verbose_name="Investment Company Name in amharic")
	owner_share	= models.FloatField(default=0,verbose_name="Owners Equity Share in %")
	bank_share	= models.FloatField(default=0,verbose_name="Bank Equity Share in %")
	capital_in_dollary	= models.FloatField(default=0,verbose_name="Capital required In Dollar")
	investment_license	= models.CharField(max_length=200, verbose_name="Investment License Code")
	issued_date	= models.DateField()
	description = models.TextField(verbose_name="Investment Project Description in English",null=True)
	description_am = models.TextField(verbose_name="Investment Project Description in amharic",null=True)
	sector	= models.CharField(choices=CAT_LIST,max_length=50, verbose_name="Project Sector")
	product_type = models.ManyToManyField(Category,related_name="project_product_types")
	site_location_name = models.CharField(verbose_name="Site location street name", max_length=200,null=True,blank=True)
	distance_f_strt	= models.FloatField(default=0,verbose_name="Distance of the Site from the Street")
	land_acquisition = models.ForeignKey(ProjectDropDownsMaster,on_delete=models.RESTRICT, related_name="land_aquisition", verbose_name="Land Acquisition",null=True,blank=True)
	project_classification	= models.ForeignKey(ProjectDropDownsMaster, on_delete=models.CASCADE,related_name="project_classification",verbose_name="Project Classification",null=True,blank=True)
	contact_person	=  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT,null=True,blank=True)
	remaining_work	= models.TextField(verbose_name="Remaining Work To be done in English ",null=True,blank=True)
	remaining_work_am	= models.TextField(verbose_name="Remaining Work To be done in amharic",null=True,blank=True)
	major_problems	= models.TextField(verbose_name="List Major Problems that need to be addressed in English",null=True,blank=True)
	major_problems_am	= models.TextField(verbose_name="List Major Problems that need to be addressed in amharic",null=True,blank=True)
	operational_time =  models.DateField(verbose_name="Planned Tme to be Operational",null=True,blank=True)
	annual_raw_material =	models.TextField(verbose_name="Annual Raw material demand and type in English",null=True,blank=True)
	annual_raw_material_am =	models.TextField(verbose_name="Annual Raw material demand and type in Amharic",null=True,blank=True)
	power_need	= models.FloatField(default=0,verbose_name="power Need in kwh",null=True,blank=True)
	water_suply	= models.FloatField(default=0,verbose_name="Water Supply",null=True,blank=True)
	cond_provided_for_wy = models.TextField(verbose_name="Special Conditions Provided for women and youth in english",null=True,blank=True)
	cond_provided_for_wy_am = models.TextField(verbose_name="Special Conditions Provided for women and youth in amharic",null=True,blank=True)
	target_market =	models.TextField(verbose_name="If  you have export  write target market (Destination)",null=True)
	env_impac_ass_doc =	models.FileField(max_length=254, verbose_name="Environmental Impact assessment document",
													help_text="Images and Pdf files less than 10MB", 
													validators=[FileExtensionValidator(allowed_extensions=allowed_file_extensions)],
													upload_to="company/project/",
													blank=True)
	capital_utilization	= models.FloatField(default=0,verbose_name="Capital Utilization")
	technology	= models.ForeignKey(ProjectDropDownsMaster,on_delete=models.RESTRICT,related_name="technology",null=True,blank=True, verbose_name="Technology going to be applied")
	automation	= models.ForeignKey(ProjectDropDownsMaster,on_delete=models.RESTRICT,related_name="automation",null=True,blank=True, verbose_name="Automation",)
	mode_of_project	= models.ForeignKey(ProjectDropDownsMaster,on_delete=models.RESTRICT,related_name="project_mode",null=True,blank=True,verbose_name="Mode of Project")
	facility_design	= models.ForeignKey(ProjectDropDownsMaster,on_delete=models.RESTRICT,related_name="facility",null=True,blank=True,verbose_name="Facility design")
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='project_created_by')
	created_date	= models.DateTimeField(auto_now_add=True)
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='project_updated_by',null=True,blank=True)
	last_updated_date	= models.DateTimeField(null=True)
	expired	= models.BooleanField(default=False)

	
class LandUsage(models.Model):
	project = models.ForeignKey(InvestmentProject,on_delete=models.CASCADE,related_name="land_usage")
	total_land_size = models.FloatField(verbose_name="Total land size in meter square")	 
	production_building = models.FloatField(verbose_name="production building in meter square")	 
	office_building = models.FloatField(verbose_name="production building in meter square")	 
	warehouse = models.FloatField(verbose_name="Ware house in meter square")	 
	other = models.FloatField(verbose_name="production building in meter square")
	timestamp = models.DateTimeField(auto_now_add=True)	 

# messages from users to a company through the contact us form
class CompanyMessage(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	name = models.CharField(max_length = 50, verbose_name='Sender Name')
	email = models.EmailField(verbose_name="Sender Email")
	message = models.TextField()
	replied = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering=['-created_date']
	
	def get_latest_reply(self):
		return CompanyMessageReply.objects.filter(message = self).first() if CompanyMessageReply.objects.filter(message = self).exists() else None

class CompanyLike(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	company = models.ForeignKey(Company, on_delete = models.CASCADE)
	created_date = models.DateField(auto_now_add = True)
	

class CompanyMessageReply(models.Model):
	message = models.ForeignKey(CompanyMessage, on_delete = models.CASCADE)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
	reply = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_date']


class CompanySubscription(models.Model):
	# users can subscribe using an email address or their FBPIDI user account
	email = models.EmailField( verbose_name = "Subscription Email.")
	created_date = models.DateTimeField(auto_now_add = True)
	


class ProjectState(models.Model):
	project = models.ForeignKey(InvestmentProject,on_delete=models.CASCADE,related_name="project_state")
	percentage_construction_performance = models.FloatField(verbose_name="percentage of construction performance" )	
	machinery_purchase_performance = models.FloatField(verbose_name="machinery Purchase Performance" )	
	factory_building_performance = models.FloatField(verbose_name="factory Building Performance")	
	machinery_installation = models.FloatField(verbose_name="machinery Installation" )	
	commissioning_work = models.FloatField(verbose_name="commissioning Work" )	
	rawmaterial_preparation = models.FloatField(verbose_name="raw Material Preparation" )	
	hremployment_training = models.FloatField(verbose_name="HR Employment Training" )	
	testproduct = models.FloatField(verbose_name="Test Product")	
	certification = models.FloatField(verbose_name="certification")	
	timestamp	= models.DateTimeField(auto_now_add=True)


class ProjectProductQuantity(models.Model):
	project = models.ForeignKey(InvestmentProject,on_delete=models.CASCADE,related_name="project_product_qty")
	product_tobe_produced = models.CharField(max_length=255,verbose_name="Product to be Produced (after implementation)")
	expected_normal_capacity = models.FloatField(default=0,verbose_name="Expected Normal Capacity (installed)")
	expected_anual_sales = models.FloatField(default=0,verbose_name="Expected Anual Sales USD (After Investment)")
	local_share = models.FloatField(default=0,verbose_name=" %\ Local Share")
	export_share = models.FloatField(default=0,verbose_name=" %\ Export Share ")
	timestamp = models.DateTimeField(auto_now_add=True)


class CompanySolution(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Title(English)")
    title_am = models.CharField(max_length=200,verbose_name="Title(Amharic)")
    description = models.TextField(verbose_name="Description(English)")
    description_am = models.TextField(verbose_name="Description(Amharic)")
    link = models.CharField(verbose_name="link",max_length=200)
    image = models.ImageField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class CompanyEvent(models.Model):
    EVENT_STATUS = [('Upcoming', 'Upcoming'),('Open', 'Open' ), ('Closed', 'Closed')]

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='companyevents', default=1)
    created_date = models.DateTimeField(auto_now_add=True, editable=False, )
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,verbose_name="Event Name(English)")
    title_am = models.CharField(max_length=200,verbose_name="Event Name(Amharic)")
    description = models.TextField(verbose_name="Description(English)")
    description_am = models.TextField(verbose_name="Description(Amharic)")
    image = models.ImageField(blank = True, null = True)
    start_date = models.DateTimeField(verbose_name="Event start date")
    end_date = models.DateTimeField(verbose_name="Event end date")
    status = models.CharField(max_length=10, verbose_name="Event status", choices=EVENT_STATUS)
    last_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.RESTRICT,null=True,blank=True)
    last_updated_date = models.DateTimeField(null=True)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date',] 
    
    def save(self):
        self.company = self.created_by.get_company()
        super(CompanyEvent, self).save()
    

    def get_image(self):
        return self.image.url if self.image else self.company.get_image()
   
    
    model_am = "ዝግጅቶች"


class EventParticipants(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(CompanyEvent, on_delete=models.CASCADE)
    patricipant_email = models.EmailField(max_length=200, blank=True)
    notify_on = models.DateField(blank=False, null=False)
    notified = models.BooleanField(verbose_name="If notification is sent = True", default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class HomePageSlider(models.Model):
	company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name="company_slider")
	slider_image = models.FileField(verbose_name="Slider Image",
				validators=[FileExtensionValidator(
					allowed_extensions=['jpg','png','jpeg']
				)],help_text="Upload images files with prefered, 1280x720px"
				)
	alt_text = models.CharField(max_length=255,verbose_name="Image Replacement Text")
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='slider_created_by')
	created_date	= models.DateTimeField(auto_now_add=True)
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='slider_updated_by',null=True,blank=True)
	last_updated_date	= models.DateTimeField(null=True)
	expired	= models.BooleanField(default=False)

	class Meta:
		ordering = ('-created_date',)



class Bank(models.Model):
    bank_name = models.CharField(verbose_name="bank name", max_length=255,)
    bank_name_am = models.CharField(verbose_name="bank name", max_length=255,default="")
    api_link = models.CharField(verbose_name="bank_api_link", max_length=255)

    def __str__(self):
        return self.bank_name


class CompanyBankAccount(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete = models.CASCADE)
    account_number = models.CharField(verbose_name="account number", max_length=30)

    def __str__(self):
        return f"{self.company.company_name}'s  {self.bank.bank_name} account"
    def get_bank_name(self):
        return f"{self.bank.bank_name}"

    class Meta:
        unique_together = (('company', 'bank','account_number'))
