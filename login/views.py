from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

from .forms import LoginForm, RegisterForm


# Create your views here.

# This method handles the sign in view
def sign_in(request):
    # If the person clicked the button to log in, this if will be true
    if request.method == 'GET':
        # If user is already logged in, returns them to their old view because they don't need to login again
        if request.user.is_authenticated:
            return redirect('map')

        # Opens Login Website
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    # If user typed in username/password, this will be true
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Checks if user/password is correct
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # messages.success(request, f'You are now logged in as {username.title()}.')
                return redirect('map')
        # if login failed
        messages.error(request, f'Invalid username or password')
        return render(request, 'login/login.html', {'form': form})


# logout button will lead to this instead
def sign_out(request):
    logout(request)
    # messages.success(request, f'You are now logged out.')
    return redirect('map')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'login/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # messages.success(request, "You have signed up successfully.")
            login(request, user)
            return redirect('map')
        else:
            return render(request, 'login/register.html', {'form': form})