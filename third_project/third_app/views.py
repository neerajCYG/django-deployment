from django.shortcuts import render
from third_app.forms import UserForm,UserProfileInfoForm


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'third_app/index.html')


@login_required
def special(request):
    return render(request, 'third_app/special.html', {})
    #return HttpResponse("You are logged in")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered= False
    print("here")
    user_form=UserForm()
    profile_form=UserProfileInfoForm()
    if request.method == "POST":
        user_form= UserForm(data=request.POST)
        profile_form= UserProfileInfoForm(data=request.POST)

        if(user_form.is_valid() and profile_form.is_valid()):
            user= user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user= user

            if 'profile_pic' in request.FILES:
                profile.profile_pic= request.FILES['profile_pic']
            profile.save()

            registered= True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        print("nothing got")
        user_form= UserForm()
        profile_form= UserProfileInfoForm()
    print(registered ) 
    return render(request, 'third_app/registration.html', 
                  context= {
                      'user_form':user_form,
                      'profile_form':profile_form,
                      'registered':registered
                  })


def user_login(request):
    
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account is not active")
    
        else:
            print("Login Failed")
            print("Username {} and password {}".format(username,password))
            return HttpResponse("Invalid login")
    
    else:
        return render(request,'third_app/login.html', context={})


# Create your views here.
