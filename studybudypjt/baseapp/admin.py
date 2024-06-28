from django.contrib import admin

# Register your models here.
from .models import Room, StackTopic, Message  

admin.site.register(Room)
admin.site.register(StackTopic)
admin.site.register(Message)
