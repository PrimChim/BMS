from django.shortcuts import render

# Create your views here.

# sign up view as an API
# sign up view as an API
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    # serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print("request.data: ", request.data)

        serializer = self.get_serializer(data=request.data)
        print("serializer: ", serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print("user: ", user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })