from django.db import models
from django.conf import settings
from django.db.models import Q
from datetime import datetime

from django.dispatch.dispatcher import receiver

    
        
class ChatMessages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "sent_messages", on_delete= models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "recieved_messages", on_delete= models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    reserve_attr0 = models.CharField(max_length=255, blank = True, null = True)
    reserve_attr1 = models.CharField(max_length=255, blank = True, null = True)
    reserve_attr2 = models.CharField(max_length=255, blank = True, null = True)

    

    def count_unread_chats(user):
        return ChatMessages.objects.filter(receiver = user, seen =False, is_active = True).count()

    def get_unread_from_sender(sender,user):
        unread_messages = ChatMessages.objects.filter(sender = sender, receiver=user, seen =False, is_active = True).order_by('-created_date')
        return {'count':unread_messages.count(), 'last_message':unread_messages.first()}
    

class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "sent_notifications", on_delete= models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "recieved_notifications", on_delete= models.CASCADE)
    notification = models.TextField()
    seen = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    reserve_attr0 = models.CharField(max_length=255, blank = True, null = True)
    reserve_attr1 = models.CharField(max_length=255, blank = True, null = True)
    reserve_attr2 = models.CharField(max_length=255, blank = True, null = True)

    def new_notifications(user):
        return Notification.objects.filter(receiver = user, seen=False, is_active = True)

    