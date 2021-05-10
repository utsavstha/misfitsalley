from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


def loginRequest(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("success")

            return redirect('posts')
        else:
            print("failed")
            print(username)
            messages.add_message(request, messages.ERROR,
                                 'Login Failed')
            return render(request, 'usersession/login.html')
    return render(request, 'usersession/login.html')


def registerRequest(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and email and password:
            user, created = User.objects.get_or_create(
                username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('posts')
            # user was created
            # set the password here
            else:
                messages.add_message(request, messages.ERROR,
                                     'User already exists')
                return render(request, 'usersession/register.html')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Registration Failed')
            return render(request, 'usersession/register.html')
    return render(request, 'usersession/register.html')


def logoutRequest(request):
    logout(request)
    return redirect('posts')
