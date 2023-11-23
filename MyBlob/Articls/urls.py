#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path

from .views import CreateArticls, RetrieveUpdateDestroyArticls

urlpatterns = [
    path('create_articles/', CreateArticls.as_view(), name="create_articles"),
    path('articlesmixin/', RetrieveUpdateDestroyArticls.as_view(), name='articlesmixin')
]
