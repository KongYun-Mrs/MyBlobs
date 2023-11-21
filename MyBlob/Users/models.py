from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Role(models.Model):
    class Meta:
        db_table = 'role'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    create_time = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))


class Users(models.Model):
    class Meta:
        db_table = 'user'

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, verbose_name="用户名", unique=False, db_index=True)
    password = models.CharField(max_length=64, db_column='password', verbose_name="密码", null=False)
    email = models.CharField(max_length=30, verbose_name="邮件")
    sex = models.IntegerField(verbose_name='性别')  # 0 man  1 woman
    score = models.IntegerField(verbose_name="分数", default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="角色", null=True)
    mobile = models.CharField(max_length=11, verbose_name="手机号", default='')
    level = models.CharField(max_length=8, verbose_name="会员", default="普通用户")
    create_time = models.DateTimeField(default=timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
