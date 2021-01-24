from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


from admin_site.models import Category, SubCategory
from product.models import Product,ProductImage,ProductPrice,Order,OrderProduct
from product.forms import SubCategoryForm,ProductCreationForm,CategoryForm
from accounts.models import User
from company.models import Company

# Create your views here.
# This is class/view is crated for displaying all categories and sub categories
class CategoryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == 'category':
            categories = Category.objects.all()
            context = {'categories':categories,'option':'category'}
        elif self.kwargs['option'] == 'sub_category':
            sub_categories = SubCategory.objects.all()
            context = {
                "sub_categories":sub_categories,'option':'sub_category'
            }
        return render(self.request,"admin/product/categories.html",context)

# This class/view is created for displaying category and sub category detail and editing
class CategoryDetail(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            category = Category.objects.get(id=self.kwargs['cat_id'])
            context = {
                'category':category,
                'edit':'edit'
            }
        elif self.kwargs['option'] == "sub_category":
            sub_category = SubCategory.objects.get(id=self.kwargs['cat_id'])
            cat_types = Category.objects.all().distinct('category_name')
            context = {
                'sub_category':sub_category,
                'categories_name':cat_types,
                'edit':'edit'
            }
        return render(self.request,"admin/product/category_form.html",context)
    
    def post(self,*args,**kwargs):
        context = {}
        message = ""
        option = ""
        if self.kwargs['option'] == "category":
            
            category = Category.objects.get(id=self.kwargs['cat_id'])
            category.category_name = self.request.POST['category_name']
            category.category_type = self.request.POST['category_type']
            category.description = self.request.POST['description']
            category.category_name_am = self.request.POST['category_name_am']
            category.category_type_am = self.request.POST['category_type']
            category.description_am = self.request.POST['description_am']
            if self.request.FILES.get('image') != None:
                category.image = self.request.FILES.get('image')
            category.save()
            message = "Category Updated Successfully"
            option = "category"
        elif self.kwargs['option'] == "sub_category":
            sub_category = SubCategory.objects.get(id=self.kwargs['cat_id'])
            sub_category.category_name = Category.objects.get(id=self.request.POST['category_name'])
            sub_category.sub_category_name = self.request.POST['sub_category_name']
            sub_category.description = self.request.POST['description']
            sub_category.sub_category_name_am = self.request.POST['sub_category_name_am']
            sub_category.description_am = self.request.POST['description_am']
            if self.request.FILES.get('image') != None:
                sub_category.image = self.request.FILES.get('image')
            sub_category.save()
            message = "Sub-Category Updated Successfully"
            option = "sub_category"
        messages.success(self.request,message)
        return redirect("admin:p_categories",option=option)

# This class/view is created for creating new categories
class CreateCategories(LoginRequiredMixin,View):
    cat_list_am = { "Food":'ምግብ',"Beverage":'መጠጥ',"Pharmaceuticals":'መድሃኒት' }
     
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            form = CategoryForm()
            context = {
                'category':"category",
                 'form':form,
            }
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm()
            context = {
                'sub_category':'sub_category',
                'form':form,
            }
        return render(self.request,"admin/product/category_form.html",context)
    
    def post(self,*args,**kwargs):
        if self.kwargs['option'] == "category":
            form = CategoryForm(self.request.POST,self.request.FILES)
            context = {
                'category':"category",
                 'form':form,
            }
            if form.is_valid():
                category = form.save(commit=False)
                category.user = self.request.user
                category.category_type_am=self.cat_list_am[form.cleaned_data.get('category_type')],
                category.save()
                messages.success(self.request,"You Created a New Category")
                return redirect("admin:p_categories",option='category')
            else:
                return render(self.request,"admin/product/category_form.html",context)
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm(self.request.POST,self.request.FILES)
            context = {
                'sub_category':'sub_category',
                'form':form,
            }
            if form.is_valid():
                sub_category = form.save(commit=False)
                sub_category.user=self.request.user
                sub_category.category_name=form.cleaned_data.get('category_name')
                sub_category.save()
                messages.success(self.request,"You Created a New Sub Category")
                return redirect("admin:p_categories", option='sub_category')
            else:
                return render(self.request,"admin/product/category_form.html",context)



class AdminProductListView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = ""
        if self.kwargs['user_type'] == 'admin':
            products = Product.objects.all()
            company = Company.objects.all()
            context = {'products':products,'companies':company}
        elif self.kwargs['user_type'] == 'provider':
            products = Product.objects.filter(user=self.request.user)
            company = Company.objects.filter(user=self.request.user)
            context = {'products':products,'companies':company}
        else:
            company = Company.objects.get(id=self.kwargs['user_type'])
            products = Product.objects.filter(user=company.user)
            context = {'products':products,'company':company}
        return render(self.request,"admin/product/product_list.html",context)

class ProductDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(Product,id=self.kwargs['id'])
        company = ""
        try:
            company = Company.objects.get(user=product.user)
        except ObjectDoesNotExist:
            company = None
        product_image = ProductImage.objects.filter(product=product)
        product_price = ProductPrice.objects.filter(product=product)
        if self.kwargs['option'] == 'edit':
            pcats = SubCategory.objects.all().exclude(id=product.category.id)
            return render(self.request,"admin/product/product_form.html",{'product':product,'pcats':pcats,'company':company,'edit':'edit'})    
        elif self.kwargs['option'] == 'view':
            return render(self.request,"admin/product/product_detail.html",{'product':product,'company':company,'product_imgs':product_image,'product_price':product_price})

    def post(self,*args,**kwargs):
        product = Product.objects.get(id=self.kwargs['id'])
        if self.kwargs['option'] == 'edit_all':
            category = SubCategory.objects.get(id=self.request.POST['category'])
            product.name=self.request.POST['name']
            product.name_am = self.request.POST['name_am']
            product.category=category
            product.description = self.request.POST['description']
            product.description_am = self.request.POST['description_am']
            if self.request.FILES.get('image') == None:
                pass
            elif self.request.FILES.get('image') != None:
                product.image = self.request.FILES.get('image')
            product.save()
            messages.success(self.request,"Successfully Edited Product")
            return redirect("admin:product_detail",id=product.id,option='view')
        else:
            product.description = self.request.POST['description']
            product.save()
            messages.success(self.request,"Successfully Edited Product")
            return redirect("admin:product_detail",id=product.id,option='view')

class AddProductImage(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        item = self.request.POST['product']
        image = self.request.FILES['image']
        product = Product.objects.get(id=item)
        product_image = ProductImage(
            product=product,image=image
        )
        product_image.save()
        messages.success(self.request,"Image Added Successfully!")
        return redirect("admin:product_detail",id=product.id,option='view')

class CreateProductView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = ProductCreationForm()
        context = {'form':form}
        return render(self.request,'admin/product/product_form.html',context)
    
    def post(self,*args,**kwargs):
        form = ProductCreationForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = self.request.user
            product.company = Company.objects.get(user=self.request.user)
            product.category = form.cleaned_data.get("category")
            product.save()
            messages.success(self.request,"Product Created Successfully!")
            return redirect("admin:index")

class CreatePrice(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        pid = self.request.POST['product']
        price = self.request.POST['price']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        product = Product.objects.get(id=pid)
        if self.request.POST['option'] == 'change':
            old_price = ProductPrice.objects.get(id=self.request.POST['priceid'])
            old_price.price = float(price)
            old_price.save()
        elif self.request.POST['option'] == 'new':
            price_obj = ProductPrice(
                user=self.request.user,
                product=product,
                price=float(price)
            )
            price_obj.save()
        messages.success(self.request,"Price Added Successfully!")
        return redirect("admin:product_detail", id=product.id,option='view')


class AddToCartView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(Product,id=kwargs['id'])
        
        order_product,created = OrderProduct.objects.get_or_create(
            product=product,
            to_company=product.company,
            user=self.request.user,
            ordered=False
        )
        order_queryset = Order.objects.filter(
            user=self.request.user,
            ordered=False
        )
        if order_queryset.exists():
            order = order_queryset[0]
            if order.products.filter(product__id=product.id).exists():
                order_product.quantity +=1
                order_product.save()
                return redirect("cart_summary")
            else:
                order.products.add(order_product)
                order.save()
                messages.success(self.request,"New Product is added to your cart")
                return redirect("cart_summary")
        else:
            order = Order.objects.create(user=self.request.user,order_date=timezone.now())
            order.products.add(order_product)
            order.save()
            messages.success(self.request,"The Order is added to your cart")
            return redirect("cart_summary")


class CartSummary(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order = Order.objects.get(user=self.request.user,ordered=False)
            products = Product.objects.all().order_by("timestamp")[:4]
            return  render(self.request,"frontpages/product/carts.html",{'orders':order,'products':products})
        except ObjectDoesNotExist:
            messages.warning(self.request,"You Do Not have active order")
            return redirect("index")


class DecrementFromCart(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(Product,id=self.kwargs['id'])
        order_qset = Order.objects.filter(user=self.request.user,ordered=False)
        if order_qset.exists():
            order = order_qset[0]
            if order.products.filter(product__id=product.id).exists():
                print("here")
                order_product = OrderProduct.objects.filter( 
                    user=self.request.user,product=product,ordered=False )[0]
                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                    return redirect("cart_summary")
                else:
                    order.products.remove(order_product)
                    messages.success(self.request,"All Items removed from your cart")
                    return redirect("index")
                
               
            else: 
                messages.warning(self.request,"This item was not in your cart")
                return redirect("index")
        else: 
            messages.warning(self.request,"You do not have order")
            return redirect("index")    

class CheckoutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        return render(self.request,"frontpages/product/checkout.html")