from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import logout

# from contacts.models import Contact

#view methods here:

def register(request):
    if request.method == 'POST': 
       # Getform values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

    # Check if passwords match
        if password == password2:
            # Check username for duplicates
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken.')
                return redirect('register')
            else:
            # Check email for duplicates
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is in use.')
                    return redirect('register')
                else:
                    #Looks good
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                #Login after register -- need to add "auth" after 'import messages'
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')    
                user.save()
                messages.success(request, 'You are now registered. Please sign in.')
                return redirect('login')
        else:   
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')    

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are logged out')
    return redirect ('index')

# @login_required
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')