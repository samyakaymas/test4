from django.urls import path 
from . import views

urlpatterns=[
    path('', views.signin, name="home"),
    path('passchange',views.change_password,name="passchange"),
    path('signup/',views.signup,name="signup"),
    path('signout/',views.signout,name="signout"),
    path('permissions/',views.change_permissions,name='permissions'),
    path('userlist/',views.userlist,name='userlist'),
    path('ajax/load/user',views.loaduser,name='loaduser'),
]