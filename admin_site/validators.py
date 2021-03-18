import os

def validate_file_extension(value):
	extn = os.path.splitext(value.name)[1]  # [0] returns the path and the filename
	valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
	if not extn.lower() in valid_extensions:
		raise ValidationError('Unsupported file extension. Expected files are pdf,doc,docx,jpg,png,xlsx,xls')

def validate_icon_extension(value):
	extn = os.path.splitext(value.name)[1] #returns the extension
	valid_extensions = ['png','jpg',]
	if not extn.lower() in valid_extensions:
		raise ValidationError('Unsupported file extension. png/jpg files are expected')

