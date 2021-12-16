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
                msg = "Login successful".format(username)
                messages.success(request, msg)
                return HttpResponseRedirect(request.path)
        
        elif "add-password" in request.POST:
            url = request.POST.get("url")
            email = request.POST.get("email")
            pwd= request.POST.get("password")
            hint= request.POST.get("hint")
            try:
                emailEncrypt = encryptText(email)
                pwdEncrypt = encryptText(pwd)
            except:
                msg = "Adding password unsuccessful"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            browser.open(url)
            siteTitle = parseTitle(browser.title())
            try:
                icons = favicon.get(url)
                if len(icons) > 1:
                    siteIcon = icons[1].url
                else:
                    siteIcon = icons[0].url
            except:
                siteIcon = None
            newPwd = Password.objects.create(
                user = request.user,
                email = emailEncrypt,
                pwd = pwdEncrypt,
                hint=hint,
                siteTitle = siteTitle,    
                siteLogo = siteIcon
            )
            msg = "Password saved"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        
        elif "delete" in request.POST:
            pwdId = request.POST.get("password-id")
            msg = "Password deleted"
            Password.objects.get(id=pwdId).delete()
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
        
        elif "update_profile" in request.POST:
            firstName = request.POST.get("first")
            secondName = request.POST.get("last")
            password = request.POST.get("password")
            user = User.objects.get(username = request.user.username)
            user.first_name = firstName
            user.last_name = secondName
            flag = False
            if password:
                user.set_password(password)
                flag = True
            user.save()
            if not flag:
                msg = "Profile updated successfully"
            else:
                msg = "Profile updated successfully. Login to continue!"
                logout(request)
            messages.success(request, msg)
            
            return HttpResponseRedirect(request.path)
        
        elif "update_password" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            hint = request.POST.get("hint")
            pwdId = request.POST.get("password-id")
            try:
                emailEncrypt = encryptText(email)
                pwdEncrypt = encryptText(password)
            except:
                msg = "Password updation unsuccessful"
                messages.error(request, msg)
                return HttpResponseRedirect(request.path)
            pwdObj = Password.objects.get(id=pwdId)
            pwdObj.email = emailEncrypt
            pwdObj.pwd = pwdEncrypt
            pwdObj.hint = hint
            pwdObj.save()
            msg = "Password updated successfully"
            messages.success(request, msg)
            return HttpResponseRedirect(request.path)
    
    if request.user.is_anonymous:
        return render(request, 'VaultPass/index.html')
    
    pwds = Password.objects.all().filter(user=request.user)
    for pwd in pwds:
        pwd.email = decryptText(pwd.email)
        pwd.password = decryptText(pwd.pwd)
    return render(request, 'VaultPass/index.html', {
        "passwords":pwds,
    })
    

def parseTitle(title):
    return title.split(':')[0]

def encryptText(text):
    try:
        return fernet.encrypt(text.encode()).decode()
    except Exception as e:
        raise e

def decryptText(text):
    try:
        return fernet.decrypt(text.encode()).decode()
    except Exception as e:
        raise e