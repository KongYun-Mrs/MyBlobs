#!/usr/bin/evn python
# -*-
import datetime

from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from Users.auth_user import AuthUsersBackends
from Users.serializers import UserSerializer, LoginSerializer


class LogIn(generics.ListAPIView):
    serializer_class = LoginSerializer  # 声明序列化器

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            auth_user = AuthUsersBackends()
            user, token = auth_user.authenticate(username=username, password=password)

            if user is not None:
                # 认证成功，执行登录操作
                user.user.last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user.user.save()
                token, created = Token.objects.get_or_create(user=user.user)
                return Response({"status": 200, 'token': token.key, "message": "login suceess!", "user_id": user.id})
            else:
                # 认证失败，处理登录失败的情况
                return Response({"status": 300, 'token': None, "message": "用户名或密码错误"})


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer  # 生命序列化器

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # save方法
            return Response({"status": 200, 'message': 'User registered successfully', 'user': serializer.data})
        else:
            return Response(serializer.errors, status=400)


class LogOutView(APIView):
    def delete(self, request):
        try:
            username = request.GET.get('username')
            user = User.objects.get(username=username)
            if user.is_authenticated:
                # 清除会话
                logout(request)
                # 清除token
                tokens = Token.objects.filter(user=user)
                tokens.delete()
                return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User is already logged out do not logged out again"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Exception occurred: {e}")
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
