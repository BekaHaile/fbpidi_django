from django.db import models
from django.conf import settings
from admin_site.models import SubCategory as subcategory

class CompanyAddressAttributes(models.Model):

	region = models.CharField(max_length=2000, verbose_name="Rigion")
	city_town = models.CharField(max_length=2000, verbose_name="City Town")
	subcity_zone = models.CharField(max_length=2000, verbose_name="Subcity zone")
	woreda = models.CharField(max_length=2000, verbose_name="Woreda")
	kebele = models.CharField(max_length=2000, verbose_name="Kebele")
	local_area = models.CharField(max_length=2000, verbose_name="Local Area")
	phone_number = models.IntegerField(max_length=2000, verbose_name="Phone Number")
	fax = models.CharField(max_length=2000, verbose_name="Fax")
 	email = models.EmailField(verbose_name="Email", max_length=255)
	facebooklink = models.CharField(verbose_name="Facebook", max_length=255)
	twiterlink = models.CharField(verbose_name="Twiter", max_length=255)
	instagramlink = models.CharField(verbose_name="Instagram", max_length=255)
	linkedinlink = models.CharField(verbose_name="Linkedin", max_length=255)
	googlelink = models.CharField(verbose_name="Google", max_length=255)


class InvestmentCompanyAttributesDatadictionary(models.Model):

	company	= models.ForeignKey(Company, on_delete=models.CASCADE)
	owner_share	= models.IntegerField(default=0)
	bank_share	= models.IntegerField(default=0)
	capital_in_dollary	= models.IntegerField(default=0)
	investment_license	= models.CharField(max_length=2000, verbose_name="Investment License")
	issued_date	= models.DateTimeField(null=False)
	sector	= models.CharField(max_length=2000, verbose_name="Sector")
	product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE) # the forenkey must change
	project_type = models.CharField(verbose_name="Project Classification", max_length=2000)
	site_location_name = models.CharField(verbose_name="Site location street name", max_length=2000)
	distance_f_strt	= models.IntegerField(default=1)
	land_acquisition = models.CharField(verbose_name="Land Acquisition", max_length=2000)
	land_usage	= models.ForeignKey(LandUsage, on_delete=models.CASCADE)
	state_of_project	=  models.ForeignKey(ProjectState, on_delete=models.CASCADE)
	remaining_work	= models.TextField(verbose_name="Remaining Work To be done")
	major_problems	= models.TextField(verbose_name="Major Problems")
	operational_time =  models.DateTimeField(null=False)
	annual_raw_material =	models.TextField(verbose_name="Annual Raw material demand and type")
	power_consumption	= models.IntegerField(default=1)
	water_suply	= models.IntegerField(default=1)
	product_quantity = models.TextField(verbose_name="Product Quantity")
	cond_provided_for_wy = models.TextField(verbose_name="Special Conditions Provided for women and youth")
	job_plan_recruited	= models.ForeignKey(JobOpportunities, on_delete=models.CASCADE)
 	education_stat	= models.ForeignKey(EducationalStatus, on_delete=models.CASCADE)
	target_market =	models.CharField(verbose_name="Market Destination", max_length=2000)
	env_impac_ass_doc =	models.FileField(upload_to = "impact/", max_length=254, verbose_name="Environmental Impact assessment document",help_text="pdf, Max size 3MB", blank=True)
	capital_utilization	= models.IntegerField(default=0)
	technology	= models.CharField(verbose_name="Technology going to be applied", max_length=2000)
	automation	= models.CharField(verbose_name="Automation", max_length=2000)
	mode_of_project	= models.CharField(verbose_name="Mode of Project", max_length=2000)
	facility_design	= models.CharField(verbose_name="Facility design", max_length=2000)
 
class Company(models.Model):

	name = models.CharField(verbose_name="name", max_length=2000)
	logo = models.FileField(upload_to = "Logo/", max_length=254, verbose_name="Logo of the company",help_text="pdf, Max size 3MB", blank=True)
	geo_location	= models.CharField(verbose_name="Geo location of the company", max_length=2000) ## geolocaion
	ownership = models.CharField(verbose_name="Owned by", max_length=2000)
	established_yr	= models.IntegerField(default=0)
	address	= models.ForeignKey(address, on_delete=models.CASCADE) # address
	contact_person	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # contact person
	investment_capital	= models.ForeignKey(InvestmentCapital, on_delete=models.CASCADE) # investment Capital
	category	= models.ForeignKey(category, on_delete=models.CASCADE) # category
	total_employees	= models.IntegerField(default=0)
	created_jobs	= models.ForeignKey(JobOpportunities, on_delete=models.CASCADE)
	employee_status	= models.ForeignKey(Employees, on_delete=models.CASCADE)
	expansion_plan	= models.TextField(verbose_name="Expansion Plan")
	certificate	= models.FileField(upload_to = "certificate/", max_length=254, verbose_name="certificate",help_text="pdf, Max size 3MB", blank=True)
	trade_license	= models.FileField(upload_to = "Trade_License/", max_length=254, verbose_name="your Trade License",help_text="pdf, Max size 3MB", blank=True)
	working_hours	= models.IntegerField(default=0)
	orgn_strct	= models.FileField(upload_to = "Organizational_Structure/", max_length=254, verbose_name="Organizational Structure",help_text="pdf, Max size 3MB", blank=True)
	femele_hign_posn	= models.IntegerField(default=0)
	female_med_posn	= models.IntegerField(default=0)
	src_amnt_inputs	= models.ForeignKey(SourceAmountIputs, on_delete=models.CASCADE)
	laboratory	= models.CharField(verbose_name="Laboratory", max_length=2000)
	lab_test_analysis	= models.TextField(verbose_name="Laboratory test analysis")
	lab_equipment	= models.TextField(verbose_name="Laboratory equipment")
	outsourced_test_param = models.CharField(verbose_name="Outsourced test parameters and contract agreements", max_length=2000)
	certification	= models.CharField(verbose_name="certification", max_length=2000)
	conducted_research	= models.TextField(verbose_name="Conducted research and development")
	new_product_developed	= models.CharField(verbose_name="New Product_Developed", max_length=2000) # under question
	management_tools = models.CharField(verbose_name="Management Tools", max_length=2000)
	market_destination	= models.ForeignKey(MarketTarget, on_delete=models.CASCADE)
	target_market	= models.ForeignKey(MarketDestination, on_delete=models.CASCADE)
	electric_power = models.BooleanField(null=False,default=False)
	water_supply = models.BooleanField(null=False,default=False)
	telecom	models.BooleanField(null=False,default=False)
	power_consumption	= models.ForeignKey(PowerConsumption, on_delete=models.CASCADE)
	marketing_department = models.BooleanField(null=False,default=False)
 	e_commerce	= models.BooleanField(null=False,default=False)
	active_database =	models.BooleanField(null=False,default=False)
	waste_trtmnt_system	= models.CharField(verbose_name="Waste Treatment and disposal system", max_length=2000)
	efluent_trtmnt_plant = models.CharField(verbose_name="Do you have effluent treatment plant", max_length=2000)
	env_mgmg_plan = models.BooleanField(null=False,default=False)
	source_of_energy = models.CharField(verbose_name="Source of energy", max_length=2000)
	gas_carb_emision = models.CharField(verbose_name="Measure of Gas/carbon emission to the environment", max_length=2000)
	compound_allot	= models.BooleanField(null=False,default=False)
	comunity_compliant	= models.CharField(verbose_name="Environmental issue compliant with the community", max_length=2000)
	env_focal_person = models.BooleanField(null=False,default=False)
	safety_profesional	 = models.BooleanField(null=False,default=False)
	notification_procedure	= models.BooleanField(null=False,default=False)
	university_linkage	= models.CharField(verbose_name="University linkage", max_length=2000)
	recall_system	= models.BooleanField(null=False,default=False)
	quality_defects	= models.TextField(verbose_name="Product Quantity")
	gas_waste_mgmnt_measure	= models.TextField(verbose_name="Measures to reduce gas and waste management")
	support_required	= models.CharField(verbose_name="Support type you need to increase production and market", max_length=2000)
	company_condition = models.CharField(verbose_name="company condition", max_length=2000)
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)
	expired	= models.BooleanField(null=False,default=False)

class InvestmentCapital(models.Model):

	machinery_cost	= models.IntegerField(null=False)
	building_cost	= models.IntegerField(null=False)
	working_capital	= models.IntegerField(null=False)
 
class SourceAmountIputs(models.Model):		
 
	import_company	= models.IntegerField(null=False)
	govt_suplied	= models.IntegerField(null=False)
	purchase_from_farmer	= models.IntegerField(null=False)
	purchase_from_union	= models.IntegerField(null=False)



class Employees(models.Model):

	TYPE = [('Permanent','Permanent'),('Temporary','Temporary'),('Foreign','Foreign')]
	employment_type	= models.CharField(verbose_name=" The Employee Type ", max_length=2000,choices=TYPE)	
	male	= models.IntegerField(null=False)	
	female	= models.IntegerField(null=False)	


class JobOpportunities(models.Model):

	JobType = [ ('Permanent','Permanent'),('Temporary','Temporary'),]
	Year	= models.IntegerField(null=False)	
	catagory = models.TextField(verbose_name="News Catagory, the choices are ", choices=JobType)
	male	= models.IntegerField(null=False)	
	female	= models.IntegerField(null=False)	
	amount_of_job	= models.IntegerField(null=False)	
	company	= models.ForeignKey(Company, on_delete=models.CASCADE)


class EducationalStatus(models.Model):		
	
	Education_type	= models.CharField(verbose_name="Education Type ", max_length=2000)		
	male	= models.IntegerField(null=False)		
	female	= models.IntegerField(null=False)		
	company	= models.ForeignKey(Company, on_delete=models.CASCADE)
		

class MarketTarget(models.Model):
	
	domestic = models.IntegerField(null=False)	
	export	= models.IntegerField(null=False)	
	Further processing factors 	= models.IntegerField(null=False)	
	Final consumers	= models.IntegerField(null=False)	
	Restaurant_and_hotels = models.IntegerField(null=False)	
	Institutions = models.IntegerField(null=False)	
	EPSA = models.IntegerField(null=False)	
	Hospitals	= models.IntegerField(null=False)	
	Agents	= models.IntegerField(null=False)	
	Wholesaler_Distributor	= models.IntegerField(null=False)	
	Retailer = models.IntegerField(null=False)	
	Other = models.IntegerField(null=False)	


class MarketDestination(models.Model):
	
	domestic = models.IntegerField(null=False)	
	export	= models.IntegerField(null=False)	
	Further processing factors 	= models.IntegerField(null=False)	
	Final consumers	= models.IntegerField(null=False)	
	Restaurant_and_hotels = models.IntegerField(null=False)	
	Institutions = models.IntegerField(null=False)	
	EPSA = models.IntegerField(null=False)	
	Hospitals	= models.IntegerField(null=False)	
	Agents	= models.IntegerField(null=False)	
	Wholesaler_Distributor	= models.IntegerField(null=False)	
	Retailer = models.IntegerField(null=False)	
	Other = models.IntegerField(null=False)	

class Product(models.Model): 					

	name	= models.CharField(verbose_name="Name of the Product ", max_length=2000)		
	category	= models.ForeignKey(subcategory, on_delete=models.CASCADE)
	description	= models.CharField(verbose_name="Description Of the product ", max_length=2000)		
	image	= models.ForeignKey(Image, on_delete=models.CASCADE)
	quantity	= models.CharField(verbose_name="Quantity", max_length=2000)		
	uom	= models.CharField(verbose_name="Unit of Measurement", max_length=2000)		 
	price	= models.ForeignKey(Price, on_delete=models.CASCADE) ## the foreignKey doesn't exist
	company	= models.ForeignKey(Company, on_delete=models.CASCADE) 
	
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
	created_date	= models.DateTimeField()		
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)		
	expired	= models.BooleanField(null=False,default=False)		


class ProductionCapacityOfASpecificProduct(models.Model):	 		

	product	= models.ForeignKey(Product, on_delete=models.CASCADE) 
	install_prdn_capacity	= models.IntegerField(null=False)		
	atn_prdn_capacity = models.IntegerField(null=False)		
	actual_prdn_capacity = models.IntegerField(null=False)		
	production_plan	= models.IntegerField(null=False)		
	extraction_rate	= models.IntegerField(null=False)		
	
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)			

class ProductImage(models.Model):	

	product	= models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(null=False,upload_to = "ProductImage/") ## 
	image_alt	= models.CharField(verbose_name="image_alt", max_length=2000)	

	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)		


class ProductTypePharmaceuticalProducts(models.Model):

	product	= models.ForeignKey(Product, on_delete=models.CASCADE)	
	brand_name	= models.CharField(verbose_name="Name of the brand", max_length=2000)		
	dosage_form	= models.CharField(verbose_name="Dosage Form", max_length=2000)		
	dose_and_packaging	= models.CharField(verbose_name="Dose and Packaging", max_length=2000)		
	therapeutic_group	= models.CharField(verbose_name="Therapeutic Group", max_length=2000)		

class AnnualInputNeedsProduct(models.Model):				

	product	= models.ForeignKey(Product, on_delete=models.CASCADE)
	is_active_input	= models.BooleanField(null=False,default=False)		
	amount	= models.IntegerField(null=False)			
	local_input	= models.IntegerField(null=False)			
	import_input	= models.IntegerField(null=False)			
	
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)	

class ProductionAndSalesPerformance(models.Model):

 	product	= models.ForeignKey(Product, on_delete=models.CASCADE)
 	activity_year	= models.IntegerField(null=False)			 
 	production_amount	= models.IntegerField(null=False)			
 	sales_amount	= models.IntegerField(null=False)			
 	sales_value	= models.IntegerField(null=False)			
	
	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)			

class PackagingType(models.Model):				 
	Pakaing_cateory=  [('primary','primary'),('secondary','secondary'),('teritiary','teritiary')]
 	product	= models.ForeignKey(Product, on_delete=models.CASCADE)
 	packaging	= models.CharField(verbose_name="packaging", max_length=2000)	 
 	category	= models.CharField(verbose_name="Therapeutic Group", max_length=200, choices=Pakaing_cateory)	 
 	local_input	= models.IntegerField(null=False)			
 	import_input	= models.IntegerField(null=False)			
 	wastage	= models.IntegerField(null=False)	

	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)		

class ProjectState(models.Model):

	percentageoconstructionperformance = models.CharField(verbose_name="percentage of construction performance", max_length=2000)	
	machineryPurchasePerformance = models.CharField(verbose_name="machinery Purchase Performance", max_length=2000)	
	factoryBuildingPerformance = models.CharField(verbose_name="factory Building Performance", max_length=2000)	
	machineryInstallation = models.CharField(verbose_name="machinery Installation", max_length=2000)	
	commissioningWork = models.CharField(verbose_name="commissioning Work", max_length=2000)	
	rawMaterialPreparation = models.CharField(verbose_name="raw Material Preparation", max_length=2000)	
	hrEmploymentTraining = models.CharField(verbose_name="HR Employment Training", max_length=2000)	
	testProduct = models.CharField(verbose_name="Test Product", max_length=2000)	
	certification = models.CharField(verbose_name="certification", max_length=2000)	

	created_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date	= models.DateTimeField()	
	last_updated_by	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	last_updated_date	= models.DateTimeField(auto_now_add=True)			
	expired	= models.BooleanField(null=False,default=False)	

class PowerConsumption(models.Model): 
	InstalledCapacity = models.CharField(verbose_name="Installed Capacity", max_length=2000)	
	Current Supplying = models.CharField(verbose_name="Current Supplying", max_length=2000)	

class LandUsage(models.Model):
	total_land_size = models.CharField(verbose_name="Total land size", max_length=2000)	 
	production_building = models.CharField(verbose_name="production building", max_length=2000)	 
	Office_building = models.CharField(verbose_name="production building", max_length=2000)	 
	warehouse = models.CharField(verbose_name="Ware house", max_length=2000)	 
	Other = models.CharField(verbose_name="production building", max_length=2000)	 
