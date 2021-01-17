from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# 
from product import models
from accounts.models import User
from company.models import Company
from collaborations.forms import CreateBlogs, CreateBlogComment, CreateFaqs
from collaborations.models import Blog, BlogComment,Faqs


from collaborations.forms import PollsForm, CreatePollForm, CreateChoiceForm
from collaborations.models import PollsQuestion, PollsResult, Choices

## Faqs
class FaqsFormView(View):
    def get(self,*args,**kwargs):
        form = CreateFaqs()
        context = {'form':form}
        return render(self.request,"admin/pages/faqs_forms.html",context)


    def post(self,*args,**kwargs):
        form = CreateFaqs(self.request.POST)
        context = {"form":form}
        if form.is_valid():
            faqs=Faqs(questions=self.request.POST['questions'],
                questions_am=self.request.POST['questions_am'],
                answers=self.request.POST['answers'],
                answers_am=self.request.POST['answers_am'])
            faqs.save()
            form = CreateFaqs()
            context = {'form':form}
            messages.success(self.request, "New Faqs Added Successfully")
            return redirect("admin:admin_Faqs")
        return render(self.request, "admin/pages/faqs_forms.html",context)


class FaqsView(View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        faqs=Faqs.objects.get(id=self.kwargs['id'])
        template_name="admin/pages/faqs_detail.html"
        context={'faq':faqs}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = CreateFaqs(self.request.POST)
        context={'form':form}
        faqs = Faqs.objects.get(id=self.kwargs['id'])
         
        faqs.questions = self.request.POST['questions']
        faqs.questions_am = self.request.POST['questions_am']
        faqs.answers = self.request.POST['answers']
        faqs.answers_am = self.request.POST['answers_am']
        messages.success(self.request, "Edited Faqs Successfully")
        faqs.save()
        return redirect("admin:admin_Faqs",option=option) 

class FaqsList(View):
    template_name = "admin/pages/faqs_forms.html"
    def get(self,*args,**kwargs):
        faqs=Faqs.objects.all()
        context = {'faqs':faqs}
        template_name = "admin/pages/faqs_list.html"
        return render(self.request, template_name,context)

    

# INDEX VIEW
class AdminIndex(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        context = dict()
        return render(self.request,"admin/index.html",context)

## blogform
class BlogForm(View):
    template_name="admin/pages/blog_form.html"
    def get(self,*args,**kwargs):
        form = CreateBlogs()
        template_name="admin/pages/blog_form.html"
        context={'form':form}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = CreateBlogs(self.request.POST,self.request.FILES)
        context={'form':form}
        if form.is_valid():
            blog = Blog()
            blog.user = self.request.user
            blog.title = self.request.POST['title']
            blog.tag = self.request.POST['tag']
            blog.content = self.request.POST['content']
            blog.title_am = self.request.POST['title_am']
            blog.tag_am = self.request.POST['tag_am']
            blog.content_am = self.request.POST['content_am']
            publish =self.request.POST['publish']
            if publish =="on":
                blog.publish=True 
            else:
                blog.publish=True

            print("-----------"+ str(blog.publish))
            blog.blogImage = form.cleaned_data.get("blogImage")
            blog.save()
            messages.success(self.request, "Added New Blog Successfully")
            form = CreateBlogs()
            context={'form':form}
            return render(self.request, "admin/pages/blog_form.html",context)
        return render(self.request, "admin/pages/blog_form.html",context)



class BlogList(View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        blogs = Blog.objects.all()
        template_name="admin/pages/blog_list.html"
        context={'blogs':blogs}
        return render(self.request, template_name,context)
# def post(self,*args,**kwargs):
#         product = models.Product.objects.get(id=self.kwargs['id'])
#         if self.kwargs['option'] == 'edit_all':
#             category = models.SubCategory.objects.get(id=self.request.POST['category'])
#             product.name=self.request.POST['name']
#             product.name_am = self.request.POST['name_am']
#             product.category=category
#             product.description = self.request.POST['description']
#             product.description_am = self.request.POST['description_am']
#             if self.request.FILES.get('image') == None:
#                 pass
#             elif self.request.FILES.get('image') != None:
#                 product.image = self.request.FILES.get('image')
#             product.save()
class BlogView(View):
    template_name="admin/pages/blog_list.html"
    def get(self,*args,**kwargs):
        blogs = Blog.objects.get(id=self.kwargs['id'])
        template_name="admin/pages/blog_detail.html"
        context={'form':blogs}
        return render(self.request, template_name,context)
    def post(self,*args,**kwargs):
        form = CreateBlogs(self.request.POST,self.request.FILES)
        context={'form':form}
        blog = Blog.objects.get(id=self.kwargs['id'])
         
        blog.title = self.request.POST['title']
        blog.tag = self.request.POST['tag']
        blog.content = self.request.POST['content']
        blog.title_am = self.request.POST['title_am']
        blog.tag_am = self.request.POST['tag_am']
        blog.content_am = self.request.POST['content_am']
        is_private = 'is_private' in self.request.POST
        if is_private == 'on':
            blog.publish = True
        else:
            blog.publish = False
        if self.request.FILES.get('blogImage') == None:
                 pass
        elif self.request.FILES.get('blogImage') != None:
                 blog.blogImage = self.request.FILES.get('blogImage')
        
        blog.save()
        messages.success(self.request, "Edited Blogs Successfully")
        return render(self.request, "admin/pages/blog_list.html",context)

class BlogCommentForm(View):
    template_name="admin/pages/blog_form.html"
    def post(self,*args,**kwargs):
        form = CreateBlogComment(self.request.POST)
        context={'form':form}
        if form.is_valid():
            comment = Blog()
            blog.title = self.request.POST['content']
            blog.user = self.request.user
            #blog.blog = 
            blog.save()
            form = CreateBlogs()
            context={'form':form}
            messages.success(self.request, "You commented on a blog")
            return render(self.request, "admin/pages/blog_form.html",context)
        return render(self.request, "admin/pages/blog_form.html",context)

# class BlogComment(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE,null=False)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False)
#     content = models.TextField(null=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

# category related views




class DeleteView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        message = ""
        if self.kwargs['model_name'] == 'category':
            category = models.Category.objects.get(id=self.kwargs['id'])
            category.delete()
            message = "Category Deleted"
            messages.success(self.request,message)
            return redirect("admin:p_categories",option='category')
        elif self.kwargs['model_name'] == 'Blog':
            Blog1 = Blog.objects.get(id=self.kwargs['id'])
            Blog1.delete()
            message ="Blog Deleted"
            messages.success(self.request,message)
            return redirect("admin:admin_Blogs")
        elif self.kwargs['model_name'] == 'Faqs':
            faqs = Faqs.objects.get(id=self.kwargs['id'])
            faqs.delete()
            message ="Faqs Deleted"
            messages.success(self.request,message)
            return redirect("admin:index")
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
        try:      
            if form.is_valid():
                poll = PollsQuestion(
                    user=self.request.user,
                    title=form.cleaned_data.get('title'),
                    title_am=form.cleaned_data.get('title_am'),
                    description=form.cleaned_data.get("description"),
                    description_am=form.cleaned_data.get('description_am'),
                    image = form.cleaned_data.get("image"),                 
                    
                )
                poll.save()
                messages.success(self.request,"Poll was Successfully Created!")
                return redirect("admin:admin_polls")
            else:
                messages.error(self.request, "Error! Poll was not Created!" )
                return redirect("admin:admin_polls")
                
        except Exception as e:
            print("44444444444444444444" , str (e))
            return redirect("admin:admin_polls")


class DetailPoll(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):  
          
        if self.kwargs['id'] :
            try:
                poll = PollsQuestion.objects.get(id = self.kwargs['id']  )
                # return render(self.request, "admin/pages/company_detail.html", {'poll':poll,})
                return render(self.request, "admin/pages/admin_poll_detail.html", {'poll':poll,})

            except Exception as e:
                print("eeeeeeeeeeeeeeeee", str(e))
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