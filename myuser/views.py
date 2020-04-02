import operator
from functools import reduce
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
import json
from .form import UserForm, UserFormRegister, UserFormAdd, UserFormEdit
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from global_login_required import login_not_required
from .models import User
from django.db.models import F, Q
from django.conf import settings
from django.core import serializers


# Create your views here.


@login_not_required
def login_view(request):
    """
    GET-获取登录界面视图并渲染验证码图片
    POST-验证前端传来的登录信息并进行登录操作
    :param request:
    :return:GET-视图
            POST-验证登录成功-{'state': 'success', 'message':'登录成功'}
                 验证登录失败-{'state': 'fail', 'message': '柜员号或者密码错误!'}
                 输入数据不符合规范-{'state': 'fail', 'message': user.errors}
    """
    if request.method == 'GET':
        # 没有采用captcha的验证码表单生成方式，使用了他的验证码图片生成结合自身的前端样式
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        return render(request, 'myuser/login.html', {'hash_key': hash_key, 'image_url': image_url})
    else:
        user = UserForm(request.POST)

        if user.is_valid():
            login_user = authenticate(**user.cleaned_data)
            if login_user:
                # Correct password, and the user is marked "active"
                login(request, login_user)
                data = {'state': 'success', 'message': '登录成功'}
                # Redirect to a success page.
                return HttpResponse(json.dumps(data))
                # return redirect("/user/index")
            else:
                return HttpResponse(json.dumps({'state': 'fail', 'message': '柜员号或者密码错误!'}))
        else:
            data = {'state': 'fail', 'message': user.errors}
            return HttpResponse(json.dumps(data))
            # return redirect("/user/login")


@login_not_required
def register_view(request):
    """
    GET-获取注册界面
    POST-验证注册表单并生成用户
    :param request:
    :return: GET-网页视图
             POST-输入数据符合格式规范-{'state': 'success', 'url': reverse('user:login')}
                  输入数据不符合规范-{'state': 'fail', 'message': user.errors}
    """
    if request.method == 'GET':
        hash_key = CaptchaStore.generate_key()
        image_url = captcha_image_url(hash_key)
        forms = UserFormRegister()
        return render(request, 'myuser/reg.html', {'hash_key': hash_key, 'image_url': image_url, 'forms': forms})
    elif request.method == 'POST':
        user = UserFormRegister(request.POST)
        data = {'state': 'success', 'url': reverse('user:login')}

        if user.is_valid():
            new_user = user.save(commit=False)
            new_user.set_password(user.cleaned_data['password'])
            new_user.save()
            return HttpResponse(json.dumps(data))

        else:
            data = {'state': 'fail', 'message': user.errors}
            return HttpResponse(json.dumps(data))


def index_view(request):
    """
    GET-返回用户列表界面
    :param request:
    :return: GET-返回视图
    """
    if request.method == 'GET':
        return render(request, 'myuser/index.html')


def user_table(request):
    """
    GET-根据传递过来的分页和筛选参数获取用户列表table展示的数据
    :param request:
    :return:示例-{"code": 0,
                "msg": "",
                "count": 1,
                "data": [{'user_code':'8287070', 'username':'方勇', 'gender':1, 'department_code':'828010',
                'department_name':'科技信息部'}]
    """
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        begin = (page - 1) * limit
        end = begin + limit - 1

        print(request.GET)

        search_item = []
        if request.GET.get('user_code'):
            search_item.append(Q(user_code__contains=request.GET.get('user_code')))
        else:
            search_item.append(Q(user_code__contains=''))

        if request.GET.get('username'):
            search_item.append(Q(username__contains=request.GET.get('username')))
        else:
            search_item.append(Q(username__contains=''))

        if request.GET.get('gender'):
            gender = request.GET.get('gender')
            if int(gender) != 0:
                search_item.append(Q(gender=int(gender)))

        if request.GET.get('department'):
            search_item.append(Q(department=request.GET.get('department')))

        user_list = User.objects.all().annotate(department_name=F('department__department_name'),
                                                department_code=F('department__department_code')). \
            values('user_code', 'username', 'gender', 'department_code', 'department_name'). \
            filter(reduce(operator.and_, search_item))

        return_msg = {
            "code": 0,
            "msg": "",
            "count": user_list.count(),
            "data": list(user_list[begin:end])
        }

        return HttpResponse(json.dumps(return_msg))


def user_logout(request):
    """
    用户注销
    :param request:
    :return: {'state': 'success', 'url': reverse('user:login')}
    """
    logout(request)
    return HttpResponse(json.dumps({'state': 'success', 'url': reverse('user:login')}))


def add_user(request):
    """
    GET-获取用户添加界面
    POST-验证添加用户表单输入合法性并添加用户
    :param request:
    :return:GET-视图
            POST-输入合法-{'state': 'success', 'message': '用户创建成功!'}
                 输入不合法-{'state': 'fail', 'message': user_form.errors}
    """
    if request.method == 'GET':
        return render(request, 'myuser/add.html')
    else:
        user_form = UserFormAdd(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(settings.INIT_PASSWORD)
            user.save()
            return HttpResponse(json.dumps({'state': 'success', 'message': '用户创建成功!'}))
        else:
            print(user_form.errors)
            return HttpResponse(json.dumps({'state': 'fail', 'message': user_form.errors}))


def edit_user(request):
    """
    GET-渲染返回界面
    POST-修改柜员号对应的用户信息
    :param request:
    :return: GET-返回界面
             POST-修改成功-{'state': 'success', 'message': '修改成功!'}
                  修改失败-{'state': 'fail', 'message': user_form.errors}
                  编辑用户不存在-{'state': 'fail', 'message': '当前编辑用户丢失，请刷新后重试!'}
    """
    if request.method == 'GET':
        user_code = request.GET.get('user_code')
        form = get_object_or_404(User, user_code=user_code)
        return render(request, 'myuser/edit.html', {'form': form})
    else:
        user_code = request.POST.get('user_code')
        try:
            user = User.objects.get(user_code=user_code)
            user_form = UserFormEdit(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()

                return HttpResponse(json.dumps({'state': 'success', 'message': '修改成功!'}))
            else:
                return HttpResponse(json.dumps({'state': 'fail', 'message': user_form.errors}))
        except User.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '当前编辑用户丢失，请刷新后重试!'}))


def del_user(request):
    """
    根据柜员号删除用户
    :param request:
    :return: 删除成功-{'state':'success', 'message':'删除成功!'}
             删除失败-{'state':'fail', 'message': '当前待删除的用户不存在，请刷新后重试!'}
    """
    user_code = request.POST.get('user_code')
    try:
        user = User.objects.get(user_code=user_code)
        user.delete()

        return HttpResponse(json.dumps({'state': 'success', 'message': '删除成功!'}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'state': 'fail', 'message': '当前待删除的用户不存在，请刷新后重试!'}))
