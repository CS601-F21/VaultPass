from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



def home(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                msg = "Username {} already exists".format(username)
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            elif User.objects.filter(email=email).exists():
                msg = "Email {} already registered".format(email)
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                User.objects.create_user(username, email, password)
                newUser = authenticate(request, username=username, password=password)
                if newUser is not None:
                    login(request, newUser)
                    msg = "Login successful"
                    messages.success(request, msg)
                    return HttpResponseRedirect(request.path)
        elif "logout" in request.POST:
            logout(request)
            msg = "Logged out"
            messages.error(request, msg)
            return HttpResponseRedirect(request.path)
            

                
    return render(request, 'VaultPass/index.html', {})
