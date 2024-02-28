from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# for customer API
from .models import Customer
from .serializers import CustomerSerializer

#register api
@api_view(['POST'])
def register_api(request):
    # If the request is a POST request, then the user is trying to register
    if request.method == 'POST':
        # Get the form data
        data = request.data.copy()

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
            user.save()
            return Response({'success': 'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

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
            user.save()
            messages.success(request, 'User Created Successfully')
            return redirect('users:login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('users:register')
    else:
        return render(request, 'users/register.html')

@api_view(['POST'])
def login_api(request):
    # If the request is a POST request, then the user is trying to login
    if request.method == 'POST':
        # Get the form data
        data = request.data.copy()

        username = data.get('username')
        password = data.get('password')
        # Authenticate the user
        user = authenticate(username=username, password=password)
        # If the user is authenticated, then login the user
        if user is not None:
            login(request, user)
            return Response({'success': 'User Logged in Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

def login_view(request):
    if request.method == 'POST':
        data = request.POST.copy()

        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin:index')
            login(request, user)
            return redirect('users:profile')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('users:login')
    else:
        return render(request, 'users/login.html')

# customer API
@api_view(['GET'])
def get_customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# add customer API, requires staff user login to add customer
@api_view(['POST'])
@login_required
def add_customer(request):
    if not request.user.is_staff:
        return Response({'error': 'You are not authorized to add customer'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'POST':
        data = request.data.copy()
        name = data.get('name')
        pan = data.get('pan')
        email = data.get('email')
        address = data.get('address')
        customer = Customer(name=name, pan=pan, email=email, address=address)
        customer.save()
        return Response({'success': 'Customer Added Successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)