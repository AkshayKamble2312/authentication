from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# signup view function
def sign_up(request):
  if request.method == "POST":
   fm = SignUpForm(request.POST)
   if fm.is_valid():
    messages.success(request,'Account Created Successfully !!')
    fm.save()
  else:
   fm = SignUpForm()
  return render(request,'auth_app/signup.html',{'form':fm})

#login view function
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully !!')
                    return HttpResponseRedirect('/profile/')
        else:                
            fm = AuthenticationForm()
        return render(request,'auth_app/userlogin.html',{'form':fm})
    else:
        return HttpResponseRedirect('/profile/')    

# profile
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm =EditAdminProfileForm(request.POST,instance=request.user)
                users = User.objects.all()
            else:    
                fm = EditUserProfileForm(request.POST,instance=request.user)
                users = None
            if fm.is_valid():
                messages.success(request,'Profile Updated !!!')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(instance=request.user)
                users = User.objects.all()
            else:     
                fm = EditUserProfileForm(instance=request.user)
                users = None
        return render (request,'auth_app/profile.html',{'name':request.user.username,'form':fm,'users':users})
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')  

def user_detail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        fm = EditAdminProfileForm(instance=pi)
        return render(request,'auth_app/userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')          