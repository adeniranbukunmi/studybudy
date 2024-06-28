from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, StackTopic, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .forms import RoomForm
from django.http import HttpResponse
# Create your views here.

# rooms=[
#     {"id":1, "name":"let learn python"},
#     {"id":2, "name":"Design with me"},
#     {"id":3, "name":"frontend developer"},
# ] 

def loginPage(request):
    page ='login'
    if request.user.is_authenticated:   #this is to make sure that the user does not login again after theyve log in
        return redirect('home')


        
    if request.method =='POST':
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'user does not exist') 
        if username and password:
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, 'username or password  does not exist') 
        else:
            messages.error(request, 'Please fill out all fields')

    context={'page':page}
    return render(request, 'baseapp/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, "baseapp/login_register.html", {'form':form})

def home(request):
    # rooms=Room.objects.all()  this will return all the stacks available
    # rooms=Room.objects.filter() will do same as .all bcos i didnt pass in parameter
    q=request.GET.get("q")  if request.GET.get("q") != None else ''    #this q is the parameter i will pass into the a-tag displaying stack list in the home.html file and the inline if statement is to return the whole stack list if there is no search

    rooms=Room.objects.filter(
        Q(stack__stacks_name__icontains=q) |
        Q(topic_name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q)
        )  #the stack is the name use to join the stackTopic together with Room and the __ is a link with the stacks_name in the stackTopic table and the Q is a module for searching any topic  available in the module .NOTE the 'i' before the contains is to make our search not to be case sensitive if i dont include 'i' and i use just contains, it will be case sensitive
    stack_list=StackTopic.objects.all()      #this will display all the stack available
    room_count=rooms.count()     #this will display the number of room available
    context={'rooms':rooms, "stackList":stack_list, "room_count":room_count}
    return render(request, "baseapp/home.html", context)


def room(request, pk):
    room=Room.objects.get(id=pk)

    # for rum in rooms:
    #     if rum.id ==int(pk):
    #         room=rum
    room_chat=room.message_set.all().order_by("-created")   #this will order the chat in descending order: meaning the last chat will be at the top this here is one to many relationship
    participants=room.participant.all()

    if request.method == "POST":
        sent_chat=Message.objects.create(
            #i can use update method instead of create : also note that the user, room_sending_msg, body is the exact name used in the message table 
            user_sending_msg=request.user,
            room_receiving_msg=room,
            body=request.POST.get("chat_body") #chat_body is the name i gave the input tag sending the chat
        )
        room.participant.add(request.user)
        return redirect('room', pk=room.id)

    context={"room":room, "room_chat":room_chat, 'participants':participants}
    

    return render(request, "baseapp/room.html", context)  #baseapp is added becos it inside the template located in the app 
    # i want to loop over all the rooms available

@login_required(login_url='/login')     #this will take user to login or register if they've not
def CreateRoom(request):
    form=RoomForm()
    if request.method == "POST":
        # print(request.POST)
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("home")


    context={'form':form}
    return render(request, "baseapp/room_form.html", context)


def  UpdateRoom(request, pk):
    room =Room.objects.get(id=pk)
    form=RoomForm(instance=room)  #to get the a pre-fill form

    if request.user != room.host:       #the host is the one in the Room table
        return HttpResponse('you are not allowed to edit this profile')
        
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context={'form':form}
    return render(request, 'baseapp/room_form.html', context)

@login_required(login_url='login')
def DeleteRoom(request, pk):
    room =Room.objects.get(id=pk)

    if request.user != room.host:       #the host is the one in the Room table
        return HttpResponse('you are not allowed to delete')
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "baseapp/delete.html", {"obj":room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room_receiving_msg.id
    if request.user != message.user_sending_msg:
        return HttpResponse("you are not allow here")
    if request.method == "POST":
        message.delete()
        return redirect("room", pk=room_id)
    return render(request, "baseapp/delete.html", {"obj":message})

