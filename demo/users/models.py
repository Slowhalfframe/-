from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    sex = (
        ('man', '男'),
        ('woman', '女'),
    )
    id = models.AutoField(primary_key=True)
    sex = models.CharField(choices=sex, default='man', null=True, blank=True, max_length=55, verbose_name='性别')
    phone = models.CharField(max_length=22, null=True, blank=True, verbose_name="手机号")
    age = models.CharField(max_length=9, null=True, blank=True, verbose_name="年龄")
    head = models.ImageField(upload_to="static/User/head", default='static/User/head/default.jpg', verbose_name="默认头像")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='关联用户')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user
