from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm
from django.contrib.auth import get_user_model

def signin(request):
    if request.user.is_authenticated and get_user_model().objects.get(pk=request.user.id).is_superuser:
        return redirect("/signup")
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

def signup(request):
    if request.user.is_authenticated and get_user_model().objects.get(pk=request.user.id).is_superuser:
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