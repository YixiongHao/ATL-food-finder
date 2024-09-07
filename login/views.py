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
            # FIX THIS REDIRECT POINTER
            return redirect('posts')

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
                messages.success(request, f'You are now logged in as {username.title()}.')
                return redirect('posts')
        # if login failed
        messages.error(request, f'Invalid username or password')
        return render(request, 'login/login.html', {'form': form})


# logout button will lead to this instead
def sign_out(request):
    logout(request)
    messages.success(request, f'You are now logged out.')
    # FIX THIS TO RETURN THEM TO ORIGINAL SITE INSTEAD OF LOGIN
    return redirect('login')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})