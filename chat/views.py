from django.shortcuts import render
from accounts.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'frontpages/chat/select_chat.html', {})

@login_required
def room(request, group_name):
    u = User.objects.get(username=group_name.split('_')[1])
    return render(request, 'frontpages/chat/chat.html', {'name': group_name})