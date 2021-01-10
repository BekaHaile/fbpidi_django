from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import PollsQuestion, Choices, PollsResult
from .forms import PollsForm
class Index(View):
    def get(self, *args, **kwargs):
        context = {}
        polls = PollsQuestion.objects.all()
        context={'polls':polls}
        return render(self.request, "frontpages/polls-list.html", context)

        # form = PollsForm()
        # context = {'form':form}
        # return render(self.request,"frontpages/polls_list_2.html",context)


    
