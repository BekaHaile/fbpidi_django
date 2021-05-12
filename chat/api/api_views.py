import json

from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView

from accounts.models import UserProfile
from accounts.api.serializers import UserInfoSerializer
from chat.models import ChatMessages
from chat.api.serializer import ChatMessagesSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from rest_framework.decorators import permission_classes, authentication_classes,api_view


#checks if a requested user does exist in the database

class check_username(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            u = get_object_or_404(UserProfile, username = request.query_params['username'])
            return JsonResponse({'result':True}, safe =False, )
        except Http404:
            related = UserProfile.objects.filter(username__icontains = request.query_params['username'])[:4]
            result = {'result':False,'related':[]}
            for u in related:
                result['related'].append( u.username )
            return JsonResponse(result, safe=False)

# list grouped chats
class CustomerChatList( APIView):
    def get(self, request):
        return Response(data={'error':False, 'chat_list':get_grouped_chats(request.user, None)})

# for the get, loads new message, for the post saves new sender message
class chat_ajax_handler(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        messages = []
        #get all unread messages(only), these are new unread messages other than those that are loaded when the user opens the chat layout page. like online chats from the other user
        print (" a chat request from",request.user)
        other_user = UserProfile.objects.get(username = request.query_params ['name'])
        q = Q( Q(sender = other_user ) & Q(receiver = request.user) & Q(seen = False)  ) 
        unread_messages = ChatMessages.objects.filter(q)
        for m in unread_messages:
            m.seen = True
            m.save()
        messages.append(ChatMessagesSerializer( unread_messages, many = True).data)
        return Response(data={'error':False, 'data':messages})
    def post(self, request):
      #save the message and send it back for the sender to be displayed
        try:
            m = ChatMessages(sender = request.user, receiver = UserProfile.objects.get(username = request.data['name']), message = request.data['message'])
            m.save()
            return Response(data={'error':False, 'data':ChatMessagesSerializer( m).data})

        except Exception as e:
            return Response(data ={'error':True, 'message':str(e)})
    

# opens the chatting page and loads saved messages
class chat_with(APIView):
    # Get request
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            other_user= UserProfile.objects.get(username=request.query_params['name'])
            if other_user == request.user:
                return Response(data={'error':True, 'message':"You can't chat with your self!"})
            
            messages_list = []

            q = Q( Q( Q(sender = other_user ) & Q(receiver = request.user) ) | 
                    Q( Q(sender = request.user) & Q(receiver = other_user) ) 
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
            return Response(data = {'error':False, 'other_user': UserInfoSerializer(other_user).data, 'old_messages':messages_list,'other_chats':other_chats })
   
            
        except Exception as e:
                print("Exception at chat with ",str(e))
                
    
             # if request.user.is_customer:
        #     return render(request, 'frontpages/chat/customer_chat_layout.html',{'other_user':other_user, 'old_messages': messages_list,'other_chats':other_chats})
        # else:    
        #     return render(request, 'admin/chat/chat_layout.html',{'other_user':other_user, 'old_messages': messages_list,'other_chats':other_chats})

   
class list_unread_messages(APIView):

        authentication_classes = [authentication.TokenAuthentication]
        permission_classes = [IsAuthenticated]

        def get(self, request): 
            try:       
                all_unread_messages = ChatMessages.objects.filter(receiver = request.user, seen =False).order_by('-created_date')        
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
            except Exception as e:
                print("#######",e)


        # return render(self.request, 'frontpages/chat/chat_list.html', {'chat_list':get_grouped_chats(self.request.user, None)})



def get_grouped_chats(user, excluded_user = None):
        if excluded_user !=None:
            to_exclude = Q( Q(receiver = excluded_user) | Q(sender = excluded_user))
            other_messages = ChatMessages.objects.filter( Q(receiver = user) | Q(sender = user)).exclude(to_exclude).order_by('-created_date')
        else:
            other_messages = ChatMessages.objects.filter( Q(receiver = user) | Q(sender = user)).order_by('-created_date')
            
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
