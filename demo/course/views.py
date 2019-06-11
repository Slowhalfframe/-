from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from . import models
from users.models import UserInfo
from django.contrib.auth.decorators import login_required


def detail(request):
    course_type = models.CourseType.objects.all()[:5]
    id = request.GET['id']
    course = models.Course.objects.get(pk=id)
    userinfo = UserInfo.objects.get(user=course.user)
    comment = models.Comment.objects.filter(course=course)
    return render(request, 'course/detail.html', {'course': course, 'userinfo': userinfo, 'course_type': course_type, 'comment': comment})


@login_required
def add_course(request):
    if request.method == 'GET':
        course_type = models.CourseType.objects.all()[:5]
        return render(request, 'course/add_course.html', {'course_type': course_type})
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        teac_content = request.POST['teac_content']
        cover_img = request.FILES['cover_img']
        course = request.FILES['course']
        type1 = request.POST['type1']
        type = models.CourseType.objects.get(pk=type1)
        print(title, content, teac_content, cover_img, course, type1)
        kejian_name = request.POST['kejian_name'].strip()
        # if len(kejian_name) <= 0:
        kejian = request.FILES['kejian']
        try:
            # 存储课件
            s_kj = models.kejian(kejian_name=kejian_name, kejian=kejian)
            s_kj.save()
            course = models.Course(title=title, course_info=content, teacher_info=teac_content, cover_img=cover_img, course=course, kj=s_kj, types=type, user=request.user)
            course.save()
        except:
            course = models.Course(title=title, course_info=content, teacher_info=teac_content, cover_img=cover_img, course=course, types=type, user=request.user)
            course.save()

        return redirect('/course/detail/?id={0}'.format(course.id))


@login_required
def update_course(request):
    course_type = models.CourseType.objects.all()[:5]
    if request.method == 'GET':
        id = request.GET['id']
        course = models.Course.objects.get(pk=id)
        return render(request, 'course/update_course.html', {'course': course, 'course_type': course_type})
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        teac_content = request.POST['teac_content']
        cover_img = request.FILES.get('cover_img', '')
        course = request.FILES.get('course', '')
        type1 = request.POST['type1']
        type = models.CourseType.objects.get(pk=type1)
        kejian_name = request.POST.get('kejian_name', '')
        kejian = request.FILES.get('kejian', '')
        id = request.POST['id']
        print(title, content, teac_content, cover_img, course, type, kejian_name, kejian)

        # 得到课程对象
        course_obj = models.Course.objects.get(pk=id)
        # 修改
        course_obj.title = title
        course_obj.course_info = content
        course_obj.teac_content = teac_content
        course_obj.types = type
        # 获取课件对象
        # kj_obj =models.kejian.objects.get()
        kj_obj = course_obj.kj
        # 没修改课件名称和课件
        if kejian_name == '' and kejian == '':
            pass
        else:
            kj_obj.kejian_name = kejian_name
            kj_obj.kejian = kejian
        # 没修过课程 和 图片
        if cover_img != '' and course != '':
            course_obj.cover_img = cover_img
            course_obj.course = course
        if cover_img != '':
            course_obj.cover_img = cover_img
        if course != '':
            course_obj.course = course
        course_obj.save()
        print('/course/detail/?id={0}'.format(course_obj.id))
        return redirect('/course/detail/?id={0}'.format(course_obj.id))


@login_required
def study(request):
    course_type = models.CourseType.objects.all()[:5]
    id = request.GET['id']
    course_video = models.Course.objects.get(pk=id)
    comment = models.Comment.objects.filter(course=course_video)
    course_video.click_num += 1
    course_video.save()
    like_course = models.Course.objects.filter(user=course_video.user)
    return render(request, 'course/study.html', {'course_type': course_type, 'course_video': course_video, 'comment': comment, 'like_course':like_course})


@login_required
def comment(request):
    print(1)
    url = request.META.get('HTTP_REFERER')
    print(url)
    coursr_id = request.POST['id']
    coursr_obj = models.Course.objects.get(pk=coursr_id)
    user = request.user
    comment_str = request.POST['comment']
    # 保存评论
    comment_obj = models.Comment(comment=comment_str, course=coursr_obj, user=user)
    comment_obj.save()
    return redirect(url)


# 下载课件
@login_required
def download(request):
    ret = {'code': 0}
    id = request.GET['id']
    course = models.Course.objects.get(pk=id)
    kejian = models.kejian.objects.get(course=course)
    path = kejian.kejian
    print(path)
    path = str(path)
    ret['data'] = path
    return JsonResponse(ret)


def collect(request):
    ret = {'code': 0}
    id = request.POST['id']
    user = request.user
    course_obj = models.Course.objects.get(pk=id)
    if request.user.is_authenticated():
        # 判断是否已经收藏
        is_collect = models.Collection.objects.filter(Q(course=course_obj) & Q(user=user))
        if len(is_collect) != 0:
            ret['code'] = 1
        else:
            course_obj.collection_num += 1
            course_obj.save()
            collect_obj = models.Collection(course=course_obj, user=user)
            collect_obj.save()
    else:
        ret['code'] = -1
    return JsonResponse(ret)


def search(request):
    course_type = models.CourseType.objects.all()[:5]
    query = request.GET['query']
    print(query)
    # 查询
    courses = models.Course.objects.filter(title__contains=query)
    print(courses)
    return render(request, 'course/search.html', {'courses': courses, 'query': query, 'course_type': course_type})


@login_required
def del_course(request):
    url = request.META.get('HTTP_REFERER')
    id = request.GET['id']
    course_obj = models.Course.objects.get(pk=id)
    if request.user == course_obj.user:
        course_obj.delete()
        print("shanchu")
    return redirect(url)


def type(request):
    course_type = models.CourseType.objects.all()[:5]
    id = request.GET['id']
    courses = models.Course.objects.filter(types_id=id)
    return render(request, 'course/type.html', {'courses': courses, 'course_type': course_type})