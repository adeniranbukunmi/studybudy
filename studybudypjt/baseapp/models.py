from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StackTopic(models.Model):
    stacks_name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.stacks_name
class Room(models.Model):  #the models.Model is d difference btw standard python class and that what make it a django model
    host=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    #the actual user that create the topic
    stack=models.ForeignKey(StackTopic, on_delete=models.SET_NULL, null=True)    #one to many relationship: a StackTopic(which is the parent) can receive many rooms(which is the instances or children i:e many people can pick a stackname annd create a room under the stack) but Room-table can allow the id of stacktopic  to appear just once on it
    topic_name=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True) #setting null to true means this field can be empty:if users are not ready to describe anything, the database should accept it.vice versa BLANK is set to true to allow form submission if this field is not provided
    participant= models.ManyToManyField(User, related_name='participant', blank=True)            #to store all the users that are currently active in a  room. eg if anyone comment in the room, the person has become a participant

    updated=models.DateTimeField(auto_now=True)             #auto_now: this is going to take a time snap  anytime something is added to the room eg if someone comment
    created=models.DateTimeField(auto_now_add=True)    #to know when the room is created. and auto_now_add is going to take a one time snap of when the rom is created: 

    class Meta:
        #  ordering= ['updated', 'created'] this will order in ascending order, meaning the new one will be last
         ordering= ['-updated', '-created']   #this will order it in descending order, the new room will be first
    def __str__(self):
        return self.topic_name
    

class Message(models.Model):
        user_sending_msg=models.ForeignKey(User, on_delete=models.CASCADE)  #one to many relationship: a user can send many messages but message-table can allow a User id to appear once on it
        room_receiving_msg=models.ForeignKey(Room, on_delete=models.CASCADE)   #one to many relationship: a Room can receive many messages but message-table can only have one Room id to appearing  on it

        body=models.TextField()
        updated=models.DateTimeField(auto_now=True) 
        created=models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.body[0:50]