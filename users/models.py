from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255, verbose_name="登录名")
    password = models.CharField(max_length=255, verbose_name="登录密码")
    nickname = models.CharField(max_length=255, verbose_name="用户昵称")

    class Meta:
        managed = True
        db_table = 'user'
        verbose_name_plural = "用户个人信息"

    def __str__(self):
        return self.username
