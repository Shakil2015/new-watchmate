from django.shortcuts import render
from user_app.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['username']= account.username
            data['email'] = account.email
            data['token'] = Token.objects.get(user=account).key
        else:
            return Response(serializer.errors)
        return Response(data,status.HTTP_201_CREATED)
@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=200)
# Create your views here.
