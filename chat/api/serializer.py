from chat.models import ChatMessages
from rest_framework import serializers
from datetime import datetime




class ChatMessagesSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField('get_sender_name')
    sender_image = serializers.SerializerMethodField('get_sender_image')
    receiver_name = serializers.SerializerMethodField('get_receiver_name')
    receiver_image = serializers.SerializerMethodField('get_receiver_image')
    time = serializers.SerializerMethodField('get_time')
    
    class Meta:
        model  = ChatMessages
        fields = ('id','message', 'sender_name', 'sender_image','receiver_name', 'receiver_image','time','seen' )
   
    def get_sender_name(self,chatmessages):
        return chatmessages.sender.username
   
    def get_receiver_name(self,chatmessages):
        return chatmessages.receiver.username
   
    
    def get_time(self, chatmessages):
        str_date_time = datetime.strftime(chatmessages.created_date , "%y/%m/%d %H:%M")
        return str_date_time
    
    def get_user_image(self,user):
        if user.profile_image:
            return user.profile_image.url
        else:
            return '/static/frontpages/images/clients/unkonwn_user_icon.png'

        #12345 This is the right way to return profile image, once the get_company() is resolved.
        # else:
        #     if user.is_staff  :
        #         return user.get_company().get_image() 
        #     else:
        #         return '/static/frontpages/images/clients/unkonwn_user_icon.png'
             

        
    def get_sender_image(self, chatmessages):
        return self.get_user_image(chatmessages.sender)
        

    def get_receiver_image(self, chatmessages):
        return self.get_user_image(chatmessages.receiver)

        

    
       
