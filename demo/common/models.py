from django.db import models
from django.contrib.auth.models import User


class Lunbo(models.Model):
    id = models.AutoField(primary_key=True)
    cover_img = models.ImageField(upload_to='static/common/cover', verbose_name="轮播图")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="轮播图修改者")

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username