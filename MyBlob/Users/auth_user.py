#!/usr/bin/env python
# -*- coding: utf-8 -*-


from hashlib import sha256

from django.contrib.auth import backends
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import Users


class AuthUsersBackends(backends.ModelBackend):
    def authenticate(self, request=None, username='', password=''):
        password_sha256 = sha256(password.encode("utf-8")).hexdigest()
        user = Users.objects.filter(username=username).first()
        if user and user.password == password_sha256:
            return (user, None)

        # 尝试 Token 验证
        auth_token = request.headers.get("Authorization")
        if auth_token:
            try:
                auth_token_prefix, auth_token_value = auth_token.split()
                token_obj = Token.objects.get(key=auth_token_value)
                user = token_obj.user
                return (user, token_obj)
            except Token.DoesNotExist:
                raise AuthenticationFailed({"detail": "身份认证信息验证错误", "status": 401, "message": "failed"})
            except ValueError:
                raise AuthenticationFailed({"detail": "身份认证信息验证错误", "status": 401, "message": "failed"})
        # 如果两种验证方式都不成功，返回 None
        return None

    def authenticate_header(self, request):
        return 'Token realm="api"'
