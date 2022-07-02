from django.shortcuts import render, redirect

from django.contrib.auth import authenticate,login, logout, update_session_auth_hash

from proapp.forms import SignUpForm, LoginForm, UserPasswordChange, UserPasswordReset

from django.contrib import messages

# --------------signup----------------

from django.contrib.auth.models import User
from proapp.models import Token
from django.conf import settings
from django.core.mail import send_mail
import uuid

# --------------------------------

def home(request):
    return render(request, 'home.html')

# --------------signup----------------

def user_signup(request):  
    if not request.user.is_authenticated:
        if request.method == 'POST':  
            form = SignUpForm(request.POST)  
            if form.is_valid():  
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                
                uid = uuid.uuid4()
                
                pro_obj = Token(user=user, token=uid)
                pro_obj.save()
                
                host = request.get_host()

                email_verification(host, user.email, uid)

                return render(request, 'email-verification/send_email_done.html')
            else:
                return render(request, 'signup.html', {'form': form}) 
        else:  
            form = SignUpForm()  
            return render(request, 'signup.html', {'form': form}) 
    else:
        return redirect('home')

def email_verification(host ,email, token):
    subject = "Verify Email"
    message = f"Hi check your link http://{host}/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_account_verify(request, token):
    pro_obj = Token.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)

    if user.is_active == False:
        user.is_active = True
        user.save()
        return render(request, 'email-verification/send_email_verified.html')
    else:
        return render(request, 'email-verification/send_email_already_verified.html')

# -------------------------login-------------------------------

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upassword = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upassword)
                login(request, user)
                messages.success(request,'User Login Successfully !')
                return redirect('home')
            else:
                return render(request, 'login.html', {'form':fm})
        else:
            fm = LoginForm()
            return render(request, 'login.html', {'form':fm})
    else:
        return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request,'User Logout Successfully !')
    return redirect('home')

# ----------------------------passwordreset-------------------------------------

def email_password_reset(host, email, token):
    subject = "Password Reset Link"
    message = f"Hi check your link http://{host}/password-reset/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_password_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  
            form = UserPasswordChange(user=request.user, data=request.POST) 
            if form.is_valid():  
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request,'Password changed Successfully !')
                return redirect('dashboard')
            else:
                return render(request, 'password-change/change_password.html', {'form': form})
        else:
            form = UserPasswordChange(user=request.user) 
            return render(request, 'password-change/change_password.html', {'form': form})
    else:
        return redirect('home')

def user_email_send(request):
    if request.method == 'POST':  
        email = request.POST['email']

        try:
            user = User.objects.filter(email=email).first()
            pro_obj = Token.objects.get(user=user)
            host = request.get_host()
            email_password_reset(host, email, pro_obj.token)
        
        except (User.DoesNotExist,Token.DoesNotExist) as e:
            messages.warning(request,'Invalid Email !')
            return render(request, 'password-change/password_reset_email.html')

        return render(request, 'password-change/password_reset_email_done.html')
    else:
        return render(request, 'password-change/password_reset_email.html')

def user_password_reset(request, token):
    pro_obj = Token.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)
    if request.method == 'POST':  
        form = UserPasswordReset(user=user, data=request.POST) 
        if form.is_valid():  
            form.save()
            return render(request, 'password-change/password_reset_done.html')
        else:
            return render(request, 'password-change/password_reset.html', {'form': form})
    else:
        form = UserPasswordReset(user=user) 
        return render(request, 'password-change/password_reset.html', {'form': form})
 