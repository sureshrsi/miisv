# accounts/views.py

from django.shortcuts import render, redirect
from .forms import SignUpForm, CustomAuthenticationForm, ProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(
                request, 'Your account has been created successfully!')
            # Redirect to the login page after signup
            return redirect('signup')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Access the validated form data
            username = form.cleaned_data.get('username')  # Corrected line
            password = form.cleaned_data.get('password')  # Corrected line
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')  # Adjust the redirect as needed
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/signin.html', {'form': form})


def signout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out..')
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    addresses = request.user.addresses.all()
    return render(request, 'accounts/profile.html', {'profile_form': profile_form, 'addresses': addresses})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})
