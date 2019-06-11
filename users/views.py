from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from . import tools
from io import BytesIO
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import models
from course.models import CourseType, Course, Collection


def sign_in(request):
    course_type = CourseType.objects.all()[:5]
    if request.method == 'GET':
        try:
            next_url = request.GET['next']
        except:
            next_url = "/"
        print(next_url)
        return render(request, 'users/sign_in.html', {"next_url": next_url, 'course_type': course_type})
    if request.method == 'POST':
        code = request.POST['code']
        if code.upper() != request.session['code'].upper():
            return render(request, 'users/sign_in.html', {"msg": "验证码不正确，请重新登录", 'course_type': course_type})
        # 删除session的验证码
        del request.session['code']

        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        islong = request.POST.get("islong", "no")
        next_url = request.POST.get("next", "/")
        print(username, password, islong, next_url)

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('登录成功')
                # user = serializers.serialize('json', user)
                request.session["LoginUser"] = user
                print('session')
                if islong == "on":
                    request.session.set_expiry(3600 * 24 * 7)
                elif islong == "no":
                    request.session.set_expiry(0)
                if next_url == '':
                    next_url = '/'
                print('nex_url', next_url)
                return redirect(next_url)
                # return render(request, 'common/index.html', {})
            else:
                print("没激活？")
        else:
            return render(request, 'users/sign_in.html', {"msg": "账户、密码错误", 'course_type': course_type})


def register(request):
    course_type = CourseType.objects.all()[:5]
    if request.method == 'GET':
        return render(request, 'users/register.html', {'course_type': course_type})
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()
        # 后台验证
        if len(password) < 6:
            return render(request, 'users/register.html', {"msg": "密码长度不足6位，请重新注册", 'course_type': course_type})
        if password != confirm_password:
            return render(request, 'users/register.html', {"msg": "两次输入密码不一致，请重新注册", 'course_type': course_type})
        try:
            # 用户名验证
            User.objects.get(email=email)
            return render(request, 'users/register.html', {"msg": "用户名已存在，请重新注册", 'course_type': course_type})
        except:
            try:
                # create_user辅助函数创建用户
                user = User.objects.create_user(password=password, username=username, email=email)
                usera = models.UserInfo(user=user)
                user.save()
                usera.save()
                return render(request, "users/sign_in.html", {"msg": "恭喜注册成功，请登录", 'course_type': course_type})
            except:
                return render(request, "users/register.html", {"msg": "注册失败，请重新注册", 'course_type': course_type})
    return render(request, 'users/register.html', {'course_type': course_type})


@login_required
def off(request):
    logout(request)
    return render(request, 'users/sign_in.html', {"msg": "您已成功退出！"})


@login_required
def user_info(request):
    print(request.user)
    user = models.UserInfo.objects.get(user=request.user)
    course_type = CourseType.objects.all()[:5]
    # 当前用户发表的课程
    all_course = Course.objects.filter(user=request.user)
    all_collection = Collection.objects.filter(user=request.user)
    return render(request, 'users/user_info.html', {'all_course':all_course ,'user': user, 'course_type': course_type, 'all_collection':all_collection})


@login_required
def edit(request):
    course_type = CourseType.objects.all()[:5]
    user = models.UserInfo.objects.get(user=request.user)
    if request.method =='GET':
        return render(request, 'users/edit.html', {'user': user, 'course_type': course_type})
    if request.method == 'POST':
        username = request.POST['username']
        age = request.POST['age']
        phone = request.POST['phone']
        sex = request.POST['man']
        print(username, age, phone, sex)
        # 判断用户名
        if len(username) <= 0:
            return render(request, 'users/edit.html', {'user': user, 'msg': '用户名太短'})
        # 修改用户名
        U = User.objects.get(pk=request.user.id)
        U.username = username
        U.save()
        # 修改其他
        userInfo = models.UserInfo.objects.get(user=request.user)
        userInfo.sex = sex
        userInfo.age = age
        userInfo.phone = phone
        userInfo.save()
        return redirect('/users/user_info/')


def code(request):
    img, code = tools.create_code()
    # 首先需要将code 保存到session 中
    request.session['code'] = code
    # 返会图片
    file = BytesIO()
    img.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")