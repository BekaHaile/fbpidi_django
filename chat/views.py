from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from chat.models import ChatGroup, ChatMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from chat.serializer import ChatMessageSerializer
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
@login_required
def index(request):
    return render(request, 'frontpages/chat/select_chat.html', {})

## checks the user type and redirect it to the correct url
    
## open chat room for given room_name
@login_required
def room(request, requested_group_name):
    #by default group_names are created as self.request.user.username + _ +the username of other user
    if request.user.username in requested_group_name or request.user.is_superuser:    
        group = ChatGroup()
        participant_names = requested_group_name.split("_") # this comes from frontpage/chat/chat.html for customer or admin/chat/chat_layout.html scripts
        for name in participant_names:
            try:
                User.objects.get(username = name)
            except Exception:
                print('############# Exception at chat.views. cannot chat with Unkonwn users  ')
                if request.user.is_customer:
                    return redirect('customer_chat_list')
                elif request.user.is_superuser:
                    return redirect('admin:index')
                
        try:
            q = Q( Q(group_name__contains = participant_names[0]),  Q(group_name__contains = participant_names[1]))
            group = get_object_or_404(ChatGroup, q )
            #update unread messages to read messages
            group_unread_messages = ChatMessage.get_unread_messages_from_group(group.group_name, request.user)
            for message in group_unread_messages:
                message.read = True
                message.save() 

        except Http404: # if group does not exist, create it
            print("HTTp 404 ", requested_group_name)
            group = ChatGroup(group_name=requested_group_name)
            group.save()
        
        except Exception as e:
            print("#### Exception at chat.views", str(e))
            return redirect('index')

        if request.user.is_customer:
            return render(request, 'frontpages/chat/chat2.html', {'name': group.group_name})
        else:         
            return render(request, 'admin/chat/chat_layout.html', {'name': group.group_name})

        
    else:
        print("!!!!!!!!!! User ,", request.user, "  is trying to see other's chat")
        return redirect ('index')

## open chat room for given reciever_name
@login_required
def chat_with(request, reciever_name):
    #by default group_names are created as self.request.user.username + _ +the username of other user
    user = request.user

    print("&&&&&&&&&&&&&&&&&&&&&&&&&& sender = ", user.username, " reciever ",reciever_name, " ", request )
    try:
            group = ChatGroup.objects.filter( Q(group_name__contains = user.username),  Q(group_name__contains = reciever_name)).first()
            if group:# if a group exists containg the usernames of the two users
                group_name = group.group_name 
                #update unread messages to read messages
                group_unread_messages = ChatMessage.get_unread_messages_from_group(group_name, user)
                for message in group_unread_messages:
                    message.read = True
                    message.save()      
            else: 
                g_name = f"{user.username}_{reciever_name}"
                group = ChatGroup(group_name=g_name)
                group.save()
            return redirect(f'/chat/{group.group_name}/')
             
            
            

    except Exception as e:
        print("#### Exception at chat.views llls", str(e))
        return redirect (request.path)

class ChatList( LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        print("+++++++++++++++++++++++++++++++it it inside!")
        return render(self.request, "frontpages/chat/chat_list.html", )
        

def get_grouped_message( list_of_messages, max_num_group):
    sender_names = []
    grouped = []
    for latest_sender_message in list_of_messages:
        if len(sender_names) < max_num_group: 
           if not latest_sender_message.sender.username in sender_names :
                new = ChatMessageSerializer(latest_sender_message).data
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
    
def get_all_grouped_message(user, num_group = None, excluded_group = None):
    all_messages = []
    q = Q( Q(chat_group__group_name__contains = user.username)  )
    
    if not excluded_group == None:
        try:
            exceluded_group = get_object_or_404(ChatGroup, group_name = excluded_group)
            all_messages = ChatMessage.objects.filter(q).exclude(chat_group__group_name = excluded_group).order_by('-timestamp')
            
        except Exception as e:
            print (" Exception at chat.views get_all grouped message ", str(e))
            all_messages = ChatMessage.objects.filter(q).order_by('-timestamp')
    else:
        all_messages = ChatMessage.objects.filter(q).order_by('-timestamp')
    max_num_group = all_messages.count() if num_group == None else num_group
    return get_grouped_message(list_of_messages = all_messages, max_num_group = max_num_group)
    