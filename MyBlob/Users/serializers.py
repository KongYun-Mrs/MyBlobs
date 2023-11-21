#!/usr/bin/evn python
# -*- coding: utf-8 -*-
import re
from hashlib import sha256

from django.contrib.auth.models import User
from rest_framework import serializers

from Users.models import Users, Role


class UserSerializer(serializers.Serializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'level', 'sex', 'score', 'mobile']

    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(max_length=30, required=True)
    password = serializers.CharField(max_length=64, required=True)
    mobile = serializers.CharField(max_length=11, required=True)
    level = serializers.CharField(default="普通用户")
    sex = serializers.IntegerField()
    score = serializers.IntegerField(default=0)

    def validate_username(self, username):
        if Users.objects.filter(username=username).first():
            raise serializers.ValidationError({"status": 400, "message": "用户名已存在"})
        return username

    def validate_mobile(self, mobile):
        # 判断手机号码是否已注册
        if Users.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError({"status": 400, "message": "手机号已存在"})

        # 判断手机号码格式是否有误
        REGEX_MOBILE = '1[358]\d{9}$|^147\d{8}$|^176\d{8}$'

        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("非法手机号码")

        return mobile

    def create(self, validated_data):
        validated_data["role"] = Role.objects.filter(name="普通用户").first()
        validated_data['password'] = sha256(validated_data["password"].encode("utf-8")).hexdigest()
        user = User.objects.create(username=validated_data.get('username'), password=validated_data.get("password"))
        validated_data["user"] = user
        custom_user = Users(**validated_data)
        custom_user.save()

        return custom_user


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = Users
        fields = ['username', 'password']

    username = serializers.CharField(max_length=30, required=True)
    password = serializers.CharField(max_length=64, required=True)
