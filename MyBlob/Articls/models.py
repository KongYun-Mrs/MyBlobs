#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.db import models

from Users.models import Users


class Comment(models.Model):
    class Meta:
        db_table = "comment"  # 评论

    id = models.AutoField(primary_key=True)
    draft_content = models.CharField(null=False, verbose_name="评论", max_length=1000)
    create_time = models.DateTimeField(default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), null=False,
                                       db_index=True)
    likes = models.IntegerField(default=0, verbose_name="点赞")
    likes_user = models.ForeignKey(Users, on_delete=models.CharField, related_name='likes_comment', default=None)


class ArticlesType(models.Model):
    class Meta:
        # 文章类别表
        db_table = 'articles_type'

    id = models.AutoField(primary_key=True)
    type = models.IntegerField(null=False)
    describe = models.CharField(max_length=128, verbose_name="描述信息")


class Aritcls(models.Model):
    class Meta:
        # 文章表
        db_table = 'articles'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, db_index=True, unique=True)
    create_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    update_time = models.DateTimeField(default=datetime.datetime.now())
    content = models.TextField(verbose_name="文章内容", null=False)
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="author_articls")
    articles_type = models.ForeignKey(ArticlesType, on_delete=models.CASCADE, related_name="type_articls")


class CommentArticles(models.Model):
    class Meta:
        db_table = "comment_articles"  # 评论关系表 多对多关系

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_comment")
    articles = models.ForeignKey(Aritcls, on_delete=models.CASCADE, related_name='ariticls_comment')
