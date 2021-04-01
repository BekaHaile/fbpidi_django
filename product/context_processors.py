from admin_site.models import Category
from product.models import SubCategory


def sectors(request):
    return{
        'sectors':['Food','Beverage','Pharmaceuticals']
    }

def sub_sectors(request):
    return {
        'sub_sectors':Category.objects.all()
    }
def product_type(request):
    return {
        'product_type':SubCategory.objects.all()
    }