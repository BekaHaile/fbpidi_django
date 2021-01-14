from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# 
from admin_site import models
from admin_site.forms import SubCategoryForm,ProductCreationForm
from accounts.models import User,Company

from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm
from collaborations.models import PollsQuestion, PollsResult, Choices

# INDEX VIEW
class AdminIndex(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = dict()
        return render(self.request,"admin/index.html",context)
# category related views

# This is class/view is crated for displaying all categories and sub categories
class CategoryView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == 'category':
            categories = models.Category.objects.all()
            context = {'categories':categories,'option':'category'}
        elif self.kwargs['option'] == 'sub_category':
            sub_categories = models.SubCategory.objects.all()
            context = {
                "sub_categories":sub_categories,'option':'sub_category'
            }
        return render(self.request,"admin/pages/categories.html",context)

# This class/view is created for displaying category and sub category detail and editing
class CategoryDetail(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            category = models.Category.objects.get(id=self.kwargs['cat_id'])
            context = {
                'category':category,
                'edit':'edit'
            }
        elif self.kwargs['option'] == "sub_category":
            sub_category = models.SubCategory.objects.get(id=self.kwargs['cat_id'])
            cat_types = models.Category.objects.all().distinct('category_name')
            context = {
                'sub_category':sub_category,
                'categories_name':cat_types,
                'edit':'edit'
            }
        return render(self.request,"admin/pages/category_form.html",context)
    
    def post(self,*args,**kwargs):
        context = {}
        message = ""
        option = ""
        if self.kwargs['option'] == "category":
            category = models.Category.objects.get(id=self.kwargs['cat_id'])
            category.category_name = self.request.POST['category_name']
            category.category_type = self.request.POST['category_type']
            category.description = self.request.POST['description']
            category.category_name_am = self.request.POST['category_name_am']
            category.category_type_am = self.request.POST['category_type']
            category.description_am = self.request.POST['description_am']
            category.save()
            message = "Category Updated Successfully"
            option = "category"
        elif self.kwargs['option'] == "sub_category":
            sub_category = models.SubCategory.objects.get(id=self.kwargs['cat_id'])
            sub_category.category_name = models.Category.objects.get(id=self.request.POST['category_name'])
            sub_category.sub_category_name = self.request.POST['sub_category_name']
            sub_category.description = self.request.POST['description']
            sub_category.sub_category_name_am = self.request.POST['sub_category_name_am']
            sub_category.description_am = self.request.POST['description_am']
            sub_category.save()
            message = "Sub-Category Updated Successfully"
            option = "sub_category"
        messages.success(self.request,message)
        return redirect("admin:p_categories",option=option)

# This class/view is created for creating new categories
class CreateCategories(LoginRequiredMixin,View):
    cat_list_am = { "Food":'ምግብ',"Beverage":'መጠጥ',"pharmaceuticals":'መድሃኒት' }
     
    def get(self,*args,**kwargs):
        context = {}
        if self.kwargs['option'] == "category":
            context = {
                'category':"category"
            }
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm()
            context = {
                'sub_category':'sub_category',
                'form':form,
            }
        return render(self.request,"admin/pages/category_form.html",context)
    
    def post(self,*args,**kwargs):
        if self.kwargs['option'] == "category":
            category = models.Category(
                user=self.request.user,
                category_name=self.request.POST['category_name'],
                category_type=self.request.POST['category_type'],
                description=self.request.POST['description'],
                category_name_am=self.request.POST['category_name_am'],
                category_type_am=self.cat_list_am[self.request.POST['category_type']],
                description_am=self.request.POST['description_am']
            ) 
            category.save()
            messages.success(self.request,"You Created a New Category")
            return redirect("admin:p_categories",option='category')
        elif self.kwargs['option'] == "sub_category":
            form = SubCategoryForm(self.request.POST)
            if form.is_valid():
                sub_category = models.SubCategory(
                    user=self.request.user,
                    category_name=form.cleaned_data.get('category_name'),
                    sub_category_name=form.cleaned_data.get('sub_category_name'),
                    description=form.cleaned_data.get('description'),
                    sub_category_name_am=form.cleaned_data.get('sub_category_name_am'),
                    description_am=form.cleaned_data.get('description_am')
                )
                sub_category.save()
                messages.success(self.request,"You Created a New Sub Category")
                return redirect("admin:p_categories", option='sub_category')



class AdminProductListView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        products = ""
        if self.kwargs['user_type'] == 'admin':
            products = models.Product.objects.all()
            company = Company.objects.all()
            context = {'products':products,'companies':company}
        elif self.kwargs['user_type'] == 'provider':
            products = models.Product.objects.filter(user=self.request.user)
            company = Company.objects.filter(user=self.request.user)
            context = {'products':products,'companies':company}
        else:
            company = Company.objects.get(id=self.kwargs['user_type'])
            products = models.Product.objects.filter(user=company.user)
            context = {'products':products,'company':company}
        return render(self.request,"admin/pages/product_list.html",context)

class ProductDetailView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        product = get_object_or_404(models.Product,id=self.kwargs['id'])
        company = ""
        try:
            company = Company.objects.get(user=product.user)
        except ObjectDoesNotExist:
            company = None
        product_image = models.ProductImage.objects.filter(product=product)
        product_price = models.ProductPrice.objects.filter(product=product)
        if self.kwargs['option'] == 'edit':
            pcats = models.SubCategory.objects.all().exclude(id=product.category.id)
            return render(self.request,"admin/pages/product_form.html",{'product':product,'pcats':pcats,'company':company,'edit':'edit'})    
        elif self.kwargs['option'] == 'view':
            return render(self.request,"admin/pages/product_detail.html",{'product':product,'company':company,'product_imgs':product_image,'product_price':product_price})

    def post(self,*args,**kwargs):
        product = models.Product.objects.get(id=self.kwargs['id'])
        if self.kwargs['option'] == 'edit_all':
            category = models.SubCategory.objects.get(id=self.request.POST['category'])
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
        product = models.Product.objects.get(id=item)
        product_image = models.ProductImage(
            product=product,image=image
        )
        product_image.save()
        messages.success(self.request,"Image Added Successfully!")
        return redirect("admin:product_detail",id=product.id,option='view')

class CreateProductView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = ProductCreationForm()
        context = {'form':form}
        return render(self.request,'admin/pages/product_form.html',context)
    
    def post(self,*args,**kwargs):
        form = ProductCreationForm(self.request.POST,self.request.FILES)
        if form.is_valid():
            product = models.Product(
                user=self.request.user,
                name=form.cleaned_data.get('name'),
                name_am=form.cleaned_data.get('name_am'),
                category=form.cleaned_data.get('category'),
                description=form.cleaned_data.get("description"),
                description_am=form.cleaned_data.get('description_am'),
                image=form.cleaned_data.get("image")
            )
            product.save()
            messages.success(self.request,"Product Created Successfully!")
            return redirect("admin:index")

class CreatePrice(LoginRequiredMixin,View):
    def post(self,*args,**kwargs):
        pid = self.request.POST['product']
        price = self.request.POST['price']
        start_date = self.request.POST['start_date']
        end_date = self.request.POST['end_date']
        product = models.Product.objects.get(id=pid)
        if self.request.POST['option'] == 'change':
            old_price = models.ProductPrice.objects.get(id=self.request.POST['priceid'])
            old_price.price = float(price)
            old_price.save()
        elif self.request.POST['option'] == 'new':
            price_obj = models.ProductPrice(
                user=self.request.user,
                product=product,
                price=float(price)
            )
            price_obj.save()
        messages.success(self.request,"Price Added Successfully!")
        return redirect("admin:product_detail", id=product.id,option='view')


class DeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['model_name'] == 'category':
            category = models.Category.objects.get(id=self.kwargs['id'])
            category.delete()
            message = "Category Deleted"
            messages.success(self.request,message)
            return redirect("admin:p_categories",option='category')
        elif self.kwargs['model_name'] == 'sub_category':
            sub_category = models.SubCategory.objects.get(id=self.kwargs['id'])
            sub_category.delete()
            message ="Sub-Category Deleted"
            messages.success(self.request,message)
            return redirect("admin:p_categories",option='sub_category')
        elif self.kwargs['model_name'] == 'user_account':
            user = User.objects.get(id=self.kwargs['id'])
            user.delete()
            message ="User Deleted"
            messages.success(self.request,message)
            return redirect("admin:users_list")
        elif self.kwargs['model_name'] == 'product':
            product = models.Product.objects.get(id=self.kwargs['id'])
            product.delete()
            message ="Product Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'company':
            company = Company.objects.get(id=self.kwargs['id'])
            company.delete()
            message ="Company Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
        elif self.kwargs['model_name'] == 'product_image':
            pdimage = models.ProductImage.objects.get(id=self.kwargs['id'])
            pdimage.delete()
            message ="Image Deleted"
            messages.success(self.request,message)
            return redirect("admin:product_detail",id=pdimage.product.id,option='view')

class Polls(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form = PollsForm()
        polls = PollsQuestion.objects.all()
        context = {'form':form, 'polls':polls}
        
        return render(self.request,'admin/pages/polls.html',context)
    
   
class CreatePoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):

        form = CreatePollForm()
        context = {'form':form}
        return render(self.request,'admin/pages/create_poll.html',context)
    
    def post(self,*args,**kwargs):
        
        form = CreatePollForm(self.request.POST)        
        if form.is_valid():
            poll = PollsQuestion(
                user=self.request.user,
                title=form.cleaned_data.get('title'),
                title_am=form.cleaned_data.get('title_am'),
                description=form.cleaned_data.get("description"),
                description_am=form.cleaned_data.get('description_am'),
                
            )
            poll.save()
            messages.success(self.request,"Poll was Successfully Created!")
            return redirect("admin:admin_polls")
        else:
            messages.error(self.request, "Error! Poll was not Created!" )
            return redirect("admin:admin_polls")

class DetailPoll(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        message = "" 
        messages.success(self.request, "ya message works")
          
          
        if self.kwargs['id'] :
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                # return render(self.request, "admin/pages/company_detail.html", {'poll':poll,})
                return render(self.request, "admin/pages/admin_poll_detail.html", {'poll':poll,})

            except Exception as e:
                print ("444444444444444444444444 error at admin.views.DetailPoll " ,str(e))
                messages.error(self.request, "Poll not found")
                return redirect("admin:admin_polls") 

        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")

class AddChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
        
        form = CreateChoiceForm()
        context = {'form':form, 'poll':poll}
        return render(self.request,'admin/pages/add_choice.html',context)
    
    def post(self,*args,**kwargs):
        form = CreateChoiceForm(self.request.POST)
        
        poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
        if form.is_valid():
            choice = Choices(
                choice_name=form.cleaned_data.get('choice_name'),
                choice_name_am=form.cleaned_data.get('choice_name_am'),
                description=form.cleaned_data.get("description"),
                description_am=form.cleaned_data.get('description_am'),     
            )
            choice.save()

            poll.choices.add(choice)
            poll.save()
            print(poll.choices.all())
            
            messages.success(self.request,"Choice Successfully Created!")
            return redirect("admin:admin_polls")

        else:
            messages.error(self.request, "Error! Choice Creation Failed! form case! " )
            return redirect("admin:admin_polls")


class EditPoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        
        pollform = CreatePollForm()
        choiceform = CreateChoiceForm()
        message.success(self.request, "ya message works")
       
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'] )
            # little verification (this verification is done at the front end, this is just for safety, like if user uses url)            
            if poll.count_votes() != 0:
                messages.error(self.request, "Couldn't Edit poll, because poll Edit has started!")
                return redirect('admin:admin_polls')

            context = {'pollform':pollform, 'choiceform':choiceform, 'poll':poll}
            context['edit'] = True
            
        except Exception as e:          
            print(str(e))
            messages.error(self.request, "Error, Couldn't Edit poll!")
            return redirect('admin:admin_polls')
    
        return render(self.request,'admin/pages/create_poll.html',context)

    def post(self,*args,**kwargs):
        
        form = CreatePollForm(self.request.POST)
        
        try:
            poll = PollsQuestion.objects.get(id = self.kwargs['id'])

        except Exception as e:
                print("error at Editpoll post", str(e))
                messages.error(self.request, "Error! Poll was not Edited!" )
                return redirect("admin:admin_polls")

        poll.title=self.request.POST['title']
        poll.title_am=self.request.POST['title_am']
        poll.description=self.request.POST["description"]
        poll.description_am=self.request.POST['description_am']
        poll.save()
        messages.success(self.request,"Poll has been Edited Successfully!")
        return redirect("admin:admin_polls")
       
class EditChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):        
        choiceform = CreateChoiceForm()
        
        try:
            choice = Choices.objects.get(id = self.request.GET['choice'][0] )
            context = { 'choiceform':choiceform, 'choice':choice}
            context['edit'] = True
            
        except Exception as e:
    
            print(str(e))
            messages.error(self.request, "Error, Couldn't Edit Choice!")
            return redirect('admin:admin_polls')
    
        return render(self.request,'admin/pages/add_choice.html',context)

    def post(self,*args,**kwargs):
        
        form = CreateChoiceForm(self.request.POST)
        
        try:
            choice = Choices.objects.get(id = self.request.POST['choice'])

        except Exception as e:
                print("error at Editpoll post", str(e))
                messages.error(self.request, "Error! Choice was not Edited!" )
                return redirect("admin:admin_polls")

        
        choice.choice_name=self.request.POST['choice_name']
        choice.choice_name_am=self.request.POST['choice_name_am']
        choice.description=self.request.POST["description"]
        choice.description_am=self.request.POST['description_am']
        choice.save()
        messages.success(self.request,"Choice has been Edited Successfully!")
        return redirect("admin:admin_polls")
       
class DeletePoll(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            poll = PollsQuestion.objects.filter(id = self.kwargs['id']  )
            if poll:
                poll.delete()
                message = "Poll Deleted Successfully"
                messages.success(self.request,message)
                return redirect("admin:admin_polls")
            else:
                messages.error(self.request, "NO such poll was found!")
                return redirect("admin:admin_polls")


        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")

class DeleteChoice(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['id'] :
            choice = Choices.objects.filter(id = self.kwargs['id']  )
            if choice:
                choice.delete()
                message = "Choice Deleted Successfully"
                messages.success(self.request, message)
                return redirect("admin:admin_polls")
            else:
                messages.error(self.request, "NO such Choice was found!")
                return redirect("admin:admin_polls")


        else:
            messages.error(self.request, "Nothing selected!")
            return redirect("admin:admin_polls")