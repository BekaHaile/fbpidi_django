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

def food_types(request):
    return {
        'food_types':SubCategory.objects.filter(category_name__category_type="Food")[:10]
    }

def beverage_types(request):
    return {
        'beverage_types':SubCategory.objects.filter(category_name__category_type="Beverage")[:10]
    }

def pharmaceutical_types(request):
    return {
        'pharmaceutical_types':SubCategory.objects.filter(category_name__category_type="Pharmaceuticals")[:10]
    }