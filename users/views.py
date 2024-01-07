from django.contrib.auth.models import User
from django.contrib import messages

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#register api
@api_view(['POST'])
def register(request):
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
def login(request):
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