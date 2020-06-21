from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, PasswordForm, PermissionForm
from django.contrib.auth import get_user_model
from django.views.generic import ListView,CreateView, UpdateView,DetailView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def signin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'index.html')
    if request.user.is_authenticated:
        return redirect('theory/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password, backend='accounts.backends.UserBackend')
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = SignInForm(request.POST)
            return render(request, 'login.html', {'form': form})
    else:
        form = SignInForm()
        return render(request, 'login.html', {'form': form})

@login_required()
def signup(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password, backend='accounts.backends.UserBackend')
                print(user)
                
                if user is not None:
                    print("NOT")
                    return render(request,'signup.html',{'form':form,'isCreated':1,'message':"User Not Created"})
                else:
                    return render(request,'signup.html',{'form':form,'isCreated':1,'message':"User Created"})
            else:
                return render(request, 'signup.html', {'form': form,'isCreated':1,'message':'Invalid Information'})
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form,'isCreated':0})
    return redirect('/')

def signout(request):
    logout(request)
    return redirect('/')

@login_required()
def change_password(request):
    if not request.user.is_superuser:
        return redirect('/')
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('user')
            user = get_user_model().objects.get(pk=int(id))
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            message = "Password Changed Successfully"
            form = PasswordForm()
            return render(request, 'password_change.html', {'form':form ,'message':message})
        else:
            form = PasswordForm()
            message = "Password Didnt Match"
            return render(request, 'password_change.html', {'form':form ,'message':message})
    else:
        form = PasswordForm()
        return render(request, 'password_change.html', {'form': form})

@login_required()
def change_permissions(request):
    if not request.user.is_superuser:
        return redirect('/')
    if request.method=="POST":
        form = PermissionForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('username')
            user = get_user_model().objects.get(pk=int(id))
            user.can_add_theory = form.cleaned_data.get('can_add_theory')
            user.can_edit_theory = form.cleaned_data.get('can_edit_theory')
            user.can_see_theory = form.cleaned_data.get('can_see_theory')
            user.can_add_tag = form.cleaned_data.get('can_add_tag')
            user.can_see_tag = form.cleaned_data.get('can_see_tag')
            user.can_add_cross = form.cleaned_data.get('can_add_cross')
            user.can_see_cross = form.cleaned_data.get('can_see_cross')
            user.save()
            form = PermissionForm()
            return render(request,'perm.html',context={'form':form,"message":"Changed Successfully"})
        else:
            form = PermissionForm()
            return render(request,'perm.html',context={'form':form,"message":"Error"})
    form = PermissionForm()
    return render(request,'perm.html',context={'form':form})

@login_required()
def loaduser(request):
    id = request.GET.get('id')
    user = get_user_model().objects.get(pk=id)
    data = {
        "add_theory":user.can_add_theory,
        "see_theory":user.can_see_theory,
        "edit_theory":user.can_edit_theory,
        "add_tag":user.can_add_tag,
        "see_tag":user.can_see_tag,
        "add_cross":user.can_add_cross,
        "see_cross":user.can_see_cross,
    }
    return JsonResponse(data)

@login_required()
def userlist(request):
    users = get_user_model().objects.all().order_by('username')
    return render(request,'userlist.html',context={"user_list":users})