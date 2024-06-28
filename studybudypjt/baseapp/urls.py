from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),
    path("room/<int:pk>/", views.room, name="room"),
    path("create_room/", views.CreateRoom, name="create_room"), 
    path("update_room/<int:pk>/", views.UpdateRoom, name="update_room"),
    path("delete_room/<int:pk>/", views.DeleteRoom, name="delete_room"),
    path("delete_message/<int:pk>/", views.deleteMessage, name="delete_message"),
]

# assunming i want to get info about a single room, such that when i click on the room i can see info on that single room, what i will do is to pass in a parameter in the url as above. note the string can be integer or anothe data type and the pk is the id coming from each room