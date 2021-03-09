from django.db import models
from accounts.models import User
from django.db.models import Q
from datetime import datetime


class ChatGroup(models.Model):
    """
    a chat group is uniquily created for two users, the group_name will be generated by 
    combaning the usernames of the two users. 
    """
    group_name = models.CharField(max_length=200, verbose_name="chat group name", unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    connected_users = models.ManyToManyField(User, related_name="connected")


    def __str__(self):
        return self.group_name

    def count_connected_users(self):
        return self.connected_users.all().count()

    def connect_user(self, user):
        print ("connecting ", user.username," on ", self.group_name)
        if user not in self.connected_users.all():
            self.connected_users.add(user) 
            self.save()
        
    def disconnect_user(self, user):
        print ("dis connecting ",user.username, " from ", self.group_name)
        if user in self.connected_users.all():
            self.connected_users.remove(user)
            self.save()
    
        


class ChatMessage(models.Model):
    chat_group = models.ForeignKey( ChatGroup, on_delete = models.CASCADE)
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    read = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return f'{self.sender.username} : {self.content}'

    
    def get_recieved_messages(user):
        return ChatMessage.objects.filter( Q(chat_group__group_name__contains = user.username) & ~Q(sender = user ) )

    def get_unread_messages_from_group(group_name, user):
        """
        gets all unread messages from a group name i.e from a specific sender to a user
        """
        return ChatMessage.objects.filter ( Q(chat_group__group_name = group_name), ~Q(sender = user) , Q( read = False))

    def unread_messages(user):
        return ChatMessage.objects.filter( Q(chat_group__group_name__contains = user.username) & ~Q(sender = user ) & Q(read = False) )

    #no of total unread message
    def count_unread_message( user):
        """
        counts total unread messages for a user
        """
        return ChatMessage.objects.filter( Q(chat_group__group_name__contains = user.username) & ~Q(sender = user ) & Q(read = False) ).count()

    #no of unread messages from a specific sender
    def count_unread_messages_from_sender(sender_name, user):
        q = Q( Q(chat_group__group_name__contains = sender.username) &  Q(chat_group__group_name__contains = user.username)& Q( read = False) & Q(sender = sender))
        return  ChatMessage.objects.filter(q).count()

    #returns latest 10 chat messages for sender and receiver
    def last_n_messages(chat_group, n = 10):
        """
        filters latest n messages, then it will reverse the order to make
        the latest message at the bottom, just like telegram,
        (n is by default 10)
        """
        latest_10 = ChatMessage.objects.filter(chat_group__group_name = chat_group).order_by('-timestamp')[:n]
        return latest_10[::-1]




    
