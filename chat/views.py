import json

from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from accounts.models import UserProfile
from chat.models import ChatMessages
from chat.api.serializer import ChatMessagesSerializer
from accounts.api.serializers import UserInfoSerializer
from admin_site.decorators import company_created,company_is_active

decorators = [never_cache, company_created(),company_is_active()]


#checks if a requested user does exist in the database
def delete_chat(request):
    try:
        data = json.loads(request.body)
        m = ChatMessages.objects.get( id=data['id'] )
        m.is_active = False
        m.save()
        return JsonResponse( {'result':True})
    except Exception as e:
        print("@@@ Exception Occured at delete_chat ",e)
        return JsonResponse({'result':False})

def check_username(request, username):
    context ={'found':False}
    try:
        u = get_object_or_404(UserProfile, username = username)
        context['found'] =True
        context['user'] = UserInfoSerializer(u).data
    except Http404:
        context['found'] = False
    query = UserProfile.objects.filter(username__icontains = username)[:7] 
    related = [] 
    for u in query:
        related.append( UserInfoSerializer(u).data )
    context['related'] = related
    return JsonResponse(context, safe=False)


@login_required
def chat_ajax_handler(request, id):
    messages = []
    if request.method == 'GET': #get all unread messages(only), these are new unread messages other than those that are loaded when the user opens the chat layout page. like online chats from the other user
        print (" a get request from",request.user)
        other_user = UserProfile.objects.get(id = id)
        q = Q( Q(sender = other_user ) & Q(receiver = request.user) & Q(seen = False)  & Q(is_active = True)) 
        unread_messages = ChatMessages.objects.filter(q)
        for m in unread_messages:
            m.seen = True
            m.save()
        messages.append(ChatMessagesSerializer( unread_messages, many = True).data)
    elif request.method == 'POST':  #save the message and send it back for the sender to be displayed
        data = json.loads(request.body)
        m = ChatMessages(sender = request.user, receiver = UserProfile.objects.get(id = id), message = data['message'])
        m.save()
        messages.append( ChatMessagesSerializer( m).data)
    return JsonResponse(messages, safe = False)
    

# opens the chatting page and loads saved messages

def chat_with(request, reciever_name):    
    try:
        other_user= UserProfile.objects.get(username=reciever_name)
        if other_user == request.user:
            messages.warning (request, "You can't Chat with your self!")
            if request.user.is_customer:
                return redirect('customer_chat_list')
            else:
                return redirect("admin:admin_chat_list")
    except Exception as e:
            print("Exception at chat with ",e)
            if request.user.is_customer:
                return redirect('customer_chat_list')
            else:
                return redirect("admin:admin_chat_list")
    
    messages_list = []
    if request.method == 'GET':
        q = Q( Q( Q(sender = other_user ) & Q(receiver = request.user) & Q(is_active = True) ) | 
               Q( Q(sender = request.user) & Q(receiver = other_user) & Q(is_active = True)) 
            )
        query_messages = ChatMessages.objects.filter(q).order_by("-created_date")
        unread = query_messages.filter( Q(sender = other_user ) & Q(receiver = request.user) & Q(seen = False))
        for m in unread:
            m.seen = True
            m.save()
        num_of_messages = unread.count() if unread.count()>=5 else 5 #set number of messages to 5 if unread messages are lesser than 5, or set z numer equal to no of unread messages
        query_messages = query_messages[:num_of_messages]
        reversed_query = query_messages[::-1]#we need -created_date to retrieve from db, and order of created_date to display for users, so we have to reverse it
        messages_list = ChatMessagesSerializer(reversed_query, many = True).data
 
    other_chats = get_grouped_chats(user=request.user, excluded_user=other_user)
    if request.user.is_customer:
        return render(request, 'frontpages/chat/customer_chat_layout.html',{'other_user':other_user, 'old_messages': messages_list,'other_chats':other_chats})
    else:    
        return render(request, 'admin/chat/chat_layout.html',{'other_user':other_user, 'old_messages': messages_list,'other_chats':other_chats})
    
@login_required    
def list_unread_messages(request):
        
        all_unread_messages = ChatMessages.objects.filter(receiver = request.user, seen =False , is_active = True).order_by('-created_date')        
        sender_names = []
        grouped_unread_messages = []
        for m in all_unread_messages:
            if not m.sender.username in sender_names:
                latest_from_sender= ChatMessagesSerializer(m).data
                count = all_unread_messages.filter(sender__username = m.sender.username).count()
                # add the number of unread messages from a 
                latest_from_sender['count'] = count 
                grouped_unread_messages.append(latest_from_sender)
                sender_names.append(m.sender.username)

        data = {'num':all_unread_messages.count(), 'unread_messages':grouped_unread_messages}
        return JsonResponse( data, safe = False)

# for the admin side the chat listing is done inside the viewcompanyprofile view 
class CustomerChatList( LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'frontpages/chat/chat_list.html', {'chat_list':get_grouped_chats(self.request.user, None)})

@method_decorator(decorators,name='dispatch')
class AdminChatList( LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            return render(self.request, 'admin/chat/admin_chat_list.html', {'chat_list':get_grouped_chats(self.request.user, None)})
        except Exception:
            return redirect('admin:error_404')

def get_grouped_chats(user, excluded_user = None):
        if excluded_user !=None:
            to_exclude = Q( Q(receiver = excluded_user) | Q(sender = excluded_user))
            other_messages = ChatMessages.objects.filter( Q(Q(receiver = user) | Q(sender = user)) & Q(is_active = True) ).exclude(to_exclude).order_by('-created_date')
        else:
            other_messages = ChatMessages.objects.filter( Q(Q(receiver = user) | Q(sender = user)) & Q(is_active = True) ).order_by('-created_date')
            
        other_user_names = []
        grouped_other_messages = []
        for m in other_messages:
            if not m.receiver.username in other_user_names and  user == m.sender :
                grouped_other_messages.append(  ChatMessagesSerializer(m).data  )
                other_user_names.append(m.receiver.username)
            elif  not m.sender.username in other_user_names and user == m.receiver :
                grouped_other_messages.append(  ChatMessagesSerializer(m).data  )
                other_user_names.append(m.sender.username)
             
        return  grouped_other_messages



        # return {'count':unread_messages.count(), 'unread_messages':}
