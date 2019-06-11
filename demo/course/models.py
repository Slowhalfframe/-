from django.db import models
from django.contrib.auth.models import User


class CourseType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, verbose_name="课程分类名称")
    info = models.TextField(verbose_name="课程分类介绍")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class kejian(models.Model):
    id = models.AutoField(primary_key=True)
    kejian_name = models.CharField(max_length=99, verbose_name="课程名称")
    kejian = models.FileField(upload_to='static/course/kejian', null=True, blank=True, verbose_name="课件")

    class Meta:
        verbose_name = '课件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.kejian_name


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=99, verbose_name="课程名称")
    course_info = models.TextField(verbose_name="课程简介")
    teacher_info = models.TextField(verbose_name="讲师简介")
    cover_img = models.ImageField(upload_to='static/course/cover', verbose_name="封面图片")
    course = models.FileField(upload_to='static/course/video', verbose_name="课程")
    types = models.ForeignKey(CourseType, on_delete=models.CASCADE, verbose_name="课程分类")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="课程作者")
    click_num = models.IntegerField(default=0, verbose_name="播放量")
    kj = models.ForeignKey(kejian, on_delete=models.CASCADE, verbose_name="课件")
    collection_num = models.IntegerField(default=0, verbose_name="收藏数量")
    # collection = models.ManyToManyField(Collection, verbose_name="关联收藏")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, verbose_name="关联课程")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="课程作者")

    class Meta:
        verbose_name = '收藏课程'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(verbose_name="评论内容")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="文章")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="评论人")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment
