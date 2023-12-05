from django.shortcuts import render
from django.contrib.auth import authenticate

from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics
from rest_framework.views import APIView

# Create your views here.
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    
    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # permission_classes = []
    
    def post(self, request: Request):
        request_data = request.data
        email = request_data.get('email')
        password = request_data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            return Response(data={ "key": user.auth_token.key, "tokens": tokens }, status=status.HTTP_200_OK)
        return Response(data = { "error": "invalid user" }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)