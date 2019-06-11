from django.shortcuts import render
from course.models import CourseType
from course.models import Course
from . import models
from django.contrib.auth.decorators import login_required


def index(request):
    course_type = CourseType.objects.all()[:5]
    # 推荐
    tj = Course.objects.all().order_by('-click_num')[:4]
    # java
    java = Course.objects.filter(types__name='java')[:4]
    # python
    python = Course.objects.filter(types__name='python')[:4]
    mysql = Course.objects.filter(types__name='mysql')[:4]
    c = Course.objects.filter(types__name='c/c++')[:4]
    html = Course.objects.filter(types__name='前端')[:4]
    # 分类ID

    # 轮播图
    lunbo = models.Lunbo.objects.all()[:5]
    return render(request, 'common/index.html', {'tj': tj, 'java': java, 'python': python, 'mysql': mysql,
                                                 'c': c, 'html': html, 'course_type': course_type, 'lunbo':lunbo})
