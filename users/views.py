from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Register 
def register(request):
    # If the request is a POST request, then the user is trying to register
    if request.method == 'POST':
        # Get the form data
        data = request.POST.copy()

        username = data.get('username')
        password = data.get('password')
        password_confirmation = data.get('password2')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        # If the passwords match, then create a new user
        if password == password_confirmation:
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            print(user)
            # Save the user
            user.save()
            # Redirect to the register page with a success message
            return render(request, 'users/register.html', {'success': 'User Created Successfully'})
        # Otherwise, the passwords do not match
        else:
            # Redirect to the registration page with an error message
            return render(request, 'users/register.html', {'error': 'Passwords do not match'})
    # Otherwise, the user is trying to access the registration page
    else:
        return render(request, 'users/register.html')