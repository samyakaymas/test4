from django.urls import path 
from . import views

urlpatterns=[
    path('', views.signin, name="home"),
    path('list/',views.UserListView.as_view(),name="user-list"),
    path('userUpdate/<int:pk>',views.ChangePassword,name="user-update"),
    path('signup/',views.signup,name="signup"),
    path('signout/',views.signout,name="signout")
]