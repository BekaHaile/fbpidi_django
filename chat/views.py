from django.shortcuts import render
from accounts.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'frontpages/chat/select_chat.html', {})

@login_required
def room(request, group_name):
    
    if request.user.is_customer:
        return render(request, 'frontpages/chat/chat.html', {'name': group_name})
    else:         
        return render(request, 'admin/chat/chat_layout.html', {'name': group_name})