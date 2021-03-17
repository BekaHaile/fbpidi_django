from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from chat.models import ChatGroup, ChatMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from chat.serializer import ChatMessagesSerializer
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages
@login_required
def index(request):
    return render(request, 'frontpages/chat/select_chat.html', {})

## checks the user type and redirect it to the correct url
    
## open chat room for given room_name
@login_required
def room(request, requested_group_name):
    return redirect("index")

## I will use rthe room method for all, and delete this method
@login_required
def chat_with(request, reciever_name):
    #by default group_names are created as self.request.user.username + _ +the username of other user
    user = request.user
    return redirect(f"/chat/{user.username}_{reciever_name}")
    
class ChatList( LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return redirect("index")
        

def get_grouped_message( list_of_messages, max_num_group):
    sender_names = []
    grouped = []
    for latest_sender_message in list_of_messages:
        if len(sender_names) < max_num_group: 
           if not latest_sender_message.sender.username in sender_names :
                new = ChatMessagesSerializer(latest_sender_message).data
                new['count'] = list_of_messages.filter(sender__username = latest_sender_message.sender.username).count()
                grouped.append(new)
                sender_names.append(latest_sender_message.sender.username)
        else:
            break
    return grouped

#returns the latest message from a sender and count of unread messages from a sender
def get_unread_grouped_messages(user):
    q = Q( Q(chat_group__group_name__contains = user.username) & Q( read = False) & ~Q(sender = user))
    unread_messages = ChatMessage.objects.filter(q).order_by('-timestamp') 
    return get_grouped_message(list_of_messages= unread_messages, max_num_group= unread_messages.count())


#returns the latest messages from different senders grouped by sender names and count of total messages from each sender
def get_recieved_grouped_messages(user, num_group = None, excluded_group = None):
    recieved_messages = []
    q = Q( Q(chat_group__group_name__contains = user.username)  & ~Q(sender = user))
    
    if not excluded_group == None:
        try:
            exceluded_group = get_object_or_404(ChatGroup, group_name = excluded_group)
            recieved_messages = ChatMessage.objects.filter(q).exclude(chat_group__group_name = excluded_group).order_by('-timestamp')
            
        except Exception as e:
            print (" Exception at chat.views get_recieved grouped message ", str(e))
            recieved_messages = ChatMessage.objects.filter(q).order_by('-timestamp')
    else:
        recieved_messages = ChatMessage.objects.filter(q).order_by('-timestamp')
    max_num_group = recieved_messages.count() if num_group == None else num_group
    return get_grouped_message(list_of_messages = recieved_messages, max_num_group = max_num_group)

# all messages grouped
def get_grouped_all_message(user, num_group = None, exceluded_group = None):
    chat_groups = ChatGroup.objects.filter(group_name__contains = user.username)      
    if not exceluded_group == None:
        try:
            exceluded_group = get_object_or_404(ChatGroup, group_name = exceluded_group)
            chat_groups = chat_groups.exclude(group_name=exceluded_group)
        except Exception as e:
            print (" Exception at chat.views get grouped all message second try", str(e))
    else:
        messages =[]
        for group in chat_groups:
            latest_message =ChatMessage.objects.filter(chat_group = group).first()
            if latest_message:
                new = ChatMessagesSerializer(latest_message).data
                new['count'] = 49
                messages.append(new)
    return messages

