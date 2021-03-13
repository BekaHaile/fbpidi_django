from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,ListView,UpdateView,CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


from admin_site.models import Category
from product.models import Product,ProductImage,ProductPrice,Order,OrderProduct,InvoiceRecord
from product.forms import SubCategoryForm,BrandForm,ProductCreationForm,CategoryForm,CheckoutForm
from accounts.models import User
from company.models import Company,SubCategory,Brand

import random
import string

def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits,k=30))

def create_invoice(invoice,user):
    return '#INV-'.join(random.choices(string.ascii_uppercase + (invoice.join(user.id))))

# This is class/view is crated for displaying all categories and sub categories 
class CategoryView(LoginRequiredMixin,ListView):
    model = Category
    template_name = "admin/product/categories.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
class CategoryDetail(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/categories/"


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

# This class/view is created for creating new categories
class CreateCategories(LoginRequiredMixin,CreateView):
    cat_list_am = { "Food":'ምግብ',"Beverage":'መጠጥ',"Pharmaceuticals":'መድሃኒት' }
    model = Category
    form_class = CategoryForm
    template_name = "admin/product/category_form_create.html"
    
    def form_valid(self,form):
        category = form.save(commit=False)
        category.created_by = self.request.user
        category.category_type_am=self.cat_list_am[form.cleaned_data.get('category_type')],
        category.save()
        messages.success(self.request,"You Created a New Category")
        return redirect("admin:categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = True
        return context

class SubCategoryView(LoginRequiredMixin,ListView):
    model = SubCategory
    template_name = "admin/product/categories.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SubCategory.objects.all()
        else:
            return SubCategory.objects.filter(company=Company.objects.get(contact_person=self.request.user))
            
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
class SubCategoryDetail(LoginRequiredMixin,UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/sub_categories/"

    def get_form_kwargs(self):
        kwargs = super(SubCategoryDetail,self).get_form_kwargs()
        kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context

# This class/view is created for creating new categories
class CreateSubCategories(LoginRequiredMixin,CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = "admin/product/category_form_create.html"
    
    def get_form_kwargs(self):
        kwargs = super(CreateSubCategories,self).get_form_kwargs()
        kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        return kwargs

    def form_valid(self,form):        
        sub_category = form.save(commit=False)
        sub_category.created_by = self.request.user
        # sub_category.category_name=form.cleaned_data.get('category_name')
        sub_category.company = Company.objects.get(contact_person=self.request.user)
        sub_category.save()
        messages.success(self.request,"You Created a New Sub Category")
        return redirect("admin:sub_categories")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_category'] = True
        return context



class BrandView(LoginRequiredMixin,ListView):
    model = Brand
    template_name = "admin/product/categories.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Brand.objects.all()
        else:
            return Brand.objects.filter(company=Company.objects.get(contact_person=self.request.user))
            
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context

# This class/view is created for displaying category and sub category detail and editing
class BrandDetail(LoginRequiredMixin,UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "admin/product/category_form_update.html"
    success_url = "/admin/brands/"

    def get_form_kwargs(self):
        kwargs = super(BrandDetail,self).get_form_kwargs()
        kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        return kwargs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context

# This class/view is created for creating new brands
class CreateBrand(LoginRequiredMixin,CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "admin/product/category_form_create.html"
    
    def get_form_kwargs(self):
        kwargs = super(CreateBrand,self).get_form_kwargs()
        kwargs.update({'company': Company.objects.get(contact_person=self.request.user)})
        return kwargs

    def form_valid(self,form):        
        brand = form.save(commit=False)
        brand.created_by = self.request.user
        brand.company = Company.objects.get(contact_person=self.request.user)
        brand.save()
        messages.success(self.request,"You Created a New Brand")
        return redirect("admin:brands")
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = True
        return context



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
        else:
            return render(self.request,'admin/product/product_form.html',{'form':form})

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
        context = {}
        order = Order.objects.get(user=self.request.user,ordered=False)
        context['order'] = order
        context['form'] = CheckoutForm()
        return render(self.request,"frontpages/product/checkout.html",context)

    
    def post(self,*args,**kwargs):
        form = CheckoutForm(self.request.POST)
        order = Order.objects.get(user=self.request.user,ordered=False)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = self.request.user
            shipping.save()
            order.shipping_address = shipping
            invoice = InvoiceRecord.create(
                user=self.request.user,
                amount=order.get_total_price()
            )
            invoice.code = create_invoice(invoice,self.request.user)
            invoice.save()
            order.invoice = invoice
            order.ordered = True
            order.save()
            return redirect("")

################### newly added , delete this comment
class ProductByCategoryView(View):
    def get(self,*args,**kwargs):
        products = Product.objects.filter(category=self.kwargs['cat_id'])
        context = {'products':products,'count':products.count()}
        return render(self.request,"frontpages/product/product_category.html",context)


class ProductByMainCategory(View):
    def get(self,*args,**kwargs):
        products = Product.objects.all()
        product_list = []
        context = {}
        if self.kwargs['option'] == "Beverage":
            for product in products:
                if product.category.category_name.category_type == "Beverage":
                    product_list.append(product)
        elif self.kwargs['option'] == "Food":
            for product in products:
                if product.category.category_name.category_type == "Food":
                    product_list.append(product)
        elif self.kwargs['option'] == "Pharmaceuticals":
            for product in products:
                if product.category.category_name.category_type == "Pharmaceuticals":
                    product_list.append(product)
        elif self.kwargs['option'] == "all":
            for product in products:
                product_list.append(product)
        context['products'] = product_list
        context['count'] = len(product_list)
        return render(self.request,"frontpages/product/product_category.html",context)

class ProductDetailView(View):
    def get(self,*args,**kwargs):
        try:
            form = ReviewForm()
            product = Product.objects.get(id=self.kwargs['id'])
            reviews = Review.objects.filter(product=product)
            images = ProductImage.objects.filter(product=product)
            context = {'product':product,'images':images,'form':form,'reviews':reviews}
            return render(self.request,'frontpages/product/product_detail.html',context)
        except ObjectDoesNotExist:
            return redirect("index")
    
    def post(self, *args,**kwargs):
        form = ReviewForm(self.request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = Product.objects.get(id=self.kwargs['id'])
            review.save()
            return redirect('product_detail',id=self.kwargs['id'])
        else:
            return redirect("product_detail",id=self.kwargs['id'])
