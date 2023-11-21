#!/usr/bin/env python
# -*- coding: utf-8 -*-


from hashlib import sha256

from django.contrib.auth import backends

from .models import Users


class AuthUsersBackends(backends.ModelBackend):
    def authenticate(self, username='', password=''):
        password_sha256 = sha256(password.encode("utf-8")).hexdigest()
        user = Users.objects.filter(username=username).first()
        if user:
            if user.password == password_sha256:
                return user
        else:
            return None
