from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages
from .forms import VendorForm



def registerVendor(request):
    if request.method == 'POST':
        #store data ad create a user
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your restaurant account was registered successfully!')
            return redirect('registerVendor')
        else:
            print(form.errors)
    form = UserForm()
    vendor_form = VendorForm()
    context = {
        'form': form,
        'vendor_form': vendor_form
    }
    return render(request, 'vendor/registerVendor.html', context=context)