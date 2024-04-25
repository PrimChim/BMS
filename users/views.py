from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from base.settings import EMAIL_HOST_USER

# for customer API
from .models import Customer, Otp
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
            if user.is_staff:
                return Response({'success': 'Admin Logged in Successfully', 'superuser': 1}, status=status.HTTP_200_OK)
            return Response({'success': 'User Logged in Successfully', 'superuser': 0}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET'])
def logout_api(request):
    # If the request is a GET request, then the user is trying to logout
    if request.method == 'GET':
        # Log the user out
        logout(request)
        return Response({'success': 'User Logged out Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

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

# update customer API, requires staff user login to update customer
@api_view(['PUT'])
@login_required
def update_customer(request, pk):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to update customer'}, status=status.HTTP_403_FORBIDDEN)
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = request.data.copy()
        name = data.get('name')
        pan = data.get('pan')
        email = data.get('email')
        address = data.get('address')
        customer.name = name
        customer.pan = pan
        customer.email = email
        customer.address = address
        customer.save()
        return Response({'success': 'Customer Updated Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

# delete customer API, requires staff user login to delete customer
@api_view(['DELETE'])
@login_required
def delete_customer(request, pk):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to delete customer'}, status=status.HTTP_403_FORBIDDEN)
    try:
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        customer.delete()
        return Response({'success': 'Customer Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

import random

@api_view(['POST'])
def forgot_password_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            Otp.objects.filter(email=email).delete()

            otp = ''.join(random.choices('0123456789', k=6))
            Otp.objects.create(email=email, otp=otp)

            subject = 'Password Reset'
            message = render_to_string('users/mailformat/reset-password.html', {'username': user.username, 'otp': otp})
            from_email = EMAIL_HOST_USER
            to_list = [email]
            # send_mail(subject, message, from_email, to_list, fail_silently=True)

            return Response({'success': 'Password reset OTP sent to your email'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password_api(request):
    if request.method == 'POST':
        email = request.data.get('email')
        otp = request.data.get('otp')
        password = request.data.get('password')

        print(request.data)
        user = User.objects.filter(email=email).first()
        if user:
            try:
                otp_obj = Otp.objects.filter(email=email, otp=otp).first()
            except Otp.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            if otp_obj:
                user.set_password(password)
                user.save()
                otp_obj.delete()
                return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def change_profile_details(request):
    if request.method == 'POST':
        data = request.data.copy()
        user = request.user
        user.username = data.get('username')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        user.save()
        return Response({'success': 'Profile Updated Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

#=========================Front End Views===========================#

def general_view(request, slug):
    slugs = ['account', 'forgot-password', 'index', 'login', 'reset-password']

    if slug not in slugs:
        return render(request, '404.html')
    if slug == '':
        return render(request, 'users/index.html')

    if slug == 'login' and request.user.is_authenticated:
        return redirect('billing:dashboard')
    return render(request, 'users/{}.html'.format(slug))
