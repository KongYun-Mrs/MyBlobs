#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.response import Response

from Users.models import Users
from .models import Aritcls, ArticlesType


class ArticlsSerializer(serializers.Serializer):
    class Meta:
        model = Aritcls
        fields = ['title', 'content', 'articles_type', 'author']

    title = serializers.CharField(max_length=128)
    content = serializers.CharField(allow_blank=True)
    articles_type = serializers.CharField(max_length=10)
    author = serializers.CharField(max_length=10)

    def validate_title(self, title):
        patterns = ['!', "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "{", '}', '[', ']', '|']
        if title in patterns:
            raise serializers.ValidationError({"message": "标题不允许存在特殊字符"})
        tile_obj = Aritcls.objects.filter(title=title).first()

        if tile_obj:
            raise serializers.ValidationError({"message": "文章title重复"})
        return title

    def validate_author(self, author):
        user = Users.objects.filter(username=author).first()
        if not user:
            raise serializers.ValidationError({"message": "发表文章的用户不存在"})
        return user

    def create(self, validated_data):
        articles_type = validated_data.get("articles_type")
        user = Users.objects.filter(username=validated_data.get("author")).first()
        if user:
            validated_data['author'] = user
        articels_type_obj = ArticlesType.objects.filter(describe=articles_type).first()

        if not articels_type_obj:
            articels_type_obj = ArticlesType.objects.filter(describe="综合").first()
            if not articels_type_obj:
                articels_type_obj = ArticlesType(describe="综合", type=9)
                articels_type_obj.save()
        validated_data["articles_type"] = articels_type_obj

        articls = Aritcls(**validated_data)
        articls.save()
        return articls

    def update(self, instance, validated_data):
        pass
