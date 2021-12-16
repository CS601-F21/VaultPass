from django.contrib.admin.sites import site
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from cryptography.fernet import Fernet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mechanize import Browser
from .models import Password
import favicon

fernet = Fernet(settings.FERNET_KEY)
browser = Browser()
browser.set_handle_robots(False)



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
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        
        elif "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            newLogin = authenticate(request, username=username, password=password)
            if newLogin is None:
                msg = "Login unsuccessful"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            else:
                login(request, newLogin)
                msg = "Welcome {}".format(username)
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            pwd= request.POST.get("password")
            emailEncrypt = fernet.encrypt(email.encode())
            pwdEncrypt = fernet.encrypt(pwd.encode())
            
            browser.open(url)
            siteTitle = browser.title()
            try:
                siteIcon = favicon.get(url)[1].url
            except:
                siteIcon = None
            newPwd = Password.objects.create(
                user = request.user,
                email = emailEncrypt.decode(),
                pwd = pwdEncrypt.decode(),
                siteTitle = siteTitle,    
                siteLogo = siteIcon
            )
            msg = "Password saved"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
    
    if request.user.is_anonymous:
        return render(request, 'VaultPass/index.html')

    pwds = Password.objects.all().filter(user=request.user)
    for pwd in pwds:
        pwd.email = fernet.decrypt(pwd.email.encode()).decode()
        pwd.password = fernet.decrypt(pwd.pwd.encode()).decode()
            
    return render(request, 'VaultPass/index.html', {
        "passwords":pwds,
    })
    
    # return render(request, 'VaultPass/index.html')
