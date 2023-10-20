from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode

from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.core.exceptions import PermissionDenied


# Create your views here.

# restrict Vendor from accessing Customer pages
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# restrict Customer from accessing Vendor pages
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)

            #create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.role = User.CUSTOMER
            user.save()
            # Send verification email to user
            mail_subject = 'Please activate your account.'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'You registered successfully!')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context=context)

def activate(request, uidb64, token):
    # activate user by setting is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated!')
        return redirect('myAccount')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect ('home')


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def logout(request):
        auth.logout(request)
        messages.info(request, 'You are now logged out')
        return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):

    return render(request, 'accounts/customerDashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # send reset password email to user
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'We have e-mailed your password reset link!')
            return redirect('login')
        else:
            messages.error(request, 'No account with that email address exists.')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate user by decoding the token primary key
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password!')
        return redirect('reset_password')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('home')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Your password has been changed!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')