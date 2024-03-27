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

# all users API, requires superuser login to view all users
@api_view(['GET'])
@login_required
def all_users(request):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to view all users'}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.all()
    data = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }
        data.append(user_data)
    return Response(data)

# user detail API, requires superuser login to view user detail
@api_view(['GET'])
@login_required
def user_detail(request, pk):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to view user detail'}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser
    }
    return Response(user_data)

# user update API, requires superuser login to update user
@api_view(['PUT'])
@login_required
def user_update(request, pk):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to update user'}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        data = request.data.copy()
        username = data.get('username')
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        is_staff = data.get('is_staff')
        is_superuser = data.get('is_superuser')
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return Response({'success': 'User Updated Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

# user delete API, requires superuser login to delete user
@api_view(['DELETE'])
@login_required
def user_delete(request, pk):
    if not request.user.is_superuser:
        return Response({'error': 'You are not authorized to delete user'}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        user.delete()
        return Response({'success': 'User Deleted Successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Request'}, status=status.HTTP_400_BAD_REQUEST)

# api views end here
# front end views start here
def general_view(request, slug):
    if slug == '':
        return render(request, 'users/index.html')
    return render(request, 'users/{}.html'.format(slug))