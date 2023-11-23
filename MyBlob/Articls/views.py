#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Aritcls
from .serializers import ArticlsSerializer


class CreateArticls(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Aritcls.objects.all()
    serializer_class = ArticlsSerializer


class RetrieveUpdateDestroyArticls(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
