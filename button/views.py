from django.shortcuts import render
from .models import Button, Membership
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from .forms import ButtonEditForm, ButtonAddForm
import json
from page.models import Page


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        try:
            page_code = Page.objects.get(menu_code='button').id
            button = Button.objects.filter(membership__rolesbutton__role_id=request.user.role.id,
                                           membership__page_id=page_code)
            button_external = list(button.filter(button_type=2).values('button_name', 'button_code', 'button_icon'))
            button_internal = list(button.filter(button_type=1).values('button_name', 'button_code', 'button_icon'))
            return render(request, 'button/index.html',
                          {'button_external': button_external, 'button_internal': button_internal})
        except Page.DoesNotExist:
            return HttpResponseNotFound()


def button_list(request):
    """
    返回按钮列表
    :param request:
    :return:GET-{"code":0, "msg":"", "count": button_value.count(), "data": list(button_value)}
    """
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        begin = (page - 1) * limit
        end = begin + limit - 1

        button_value = Button.objects.all().extra(
            select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m-%%d %%H:%%i:%%s')"}).values('id',
                                                                                                  'button_name',
                                                                                                  'button_code',
                                                                                                  'button_type',
                                                                                                  'button_icon',
                                                                                                  'create_time',
                                                                                                  'status')[begin:end]

        return_msg = {
            "code": 0,
            "msg": "",
            "count": button_value.count(),
            "data": list(button_value)
        }
        print(return_msg)

        return HttpResponse(json.dumps(return_msg, indent=4, sort_keys=True, default=str))


def del_button(request):
    if request.method == 'POST':
        button_id = request.POST.get('button_id')
        try:
            button = Button.objects.get(pk=button_id)
            button.delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '按钮删除成功!'}))
        except Button.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '请求删除的按钮ID不存在，请刷新后再进行尝试!'}))


def edit_button(request):
    if request.method == 'POST':
        button_id = request.POST.get('id')
        try:
            button = Button.objects.get(pk=button_id)
            button_form = ButtonEditForm(request.POST, instance=button)
            if button_form.is_valid():
                button_form.save()
                return HttpResponse(json.dumps({'state': 'success', 'message': '编辑按钮成功!'}))
            else:
                return HttpResponse(json.dumps({'state': 'fail', 'message': button_form.errors}))
        except Button.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '编辑的按钮ID不存在，请刷新后重试!'}))
    else:
        button_id = request.GET.get('button_id')
        button = get_object_or_404(Button, pk=button_id)
        button_form = ButtonAddForm(instance=button)
        return render(request, 'button/edit.html', {'form': button_form, 'id': button_id})


def add_button(request):
    if request.method == 'POST':
        button_form = ButtonAddForm(request.POST)
        if button_form.is_valid():
            button_form.save()
            return HttpResponse(json.dumps({'state': 'success', 'message': '添加按钮成功!'}))
        else:
            return HttpResponse(json.dumps({'state': 'fail', 'message': button_form.errors}))
    else:
        button = ButtonAddForm()
        return render(request, 'button/add.html', {'form': button})


def button_distribute(request):
    if request.method == 'GET':
        page_id = request.GET.get('page_id')
        if page_id:
            button_gather = Button.objects.all()
            button_checked = list(Button.objects.filter(membership__page_id=page_id).values_list('id', flat=True))
            return render(request, 'button/button_list.html',
                          {'form': button_gather, 'checked': button_checked, 'page_id': page_id})
        else:
            return HttpResponseNotFound()
    else:
        page_id = request.POST.get('page_id')
        if page_id:
            page = Page.objects.get(pk=page_id)
            button_old_list = list(Button.objects.filter(membership__page=page).values_list('id', flat=True))
            print(button_old_list)
            print(json.loads(request.POST.get('button_id')))

            for id in json.loads(request.POST.get('button_id')):
                if button_old_list.count(id):
                    button_old_list.remove(id)
                else:
                    button = Button.objects.get(pk=id)
                    membership = Membership.objects.update_or_create(page=page, button=button)
            for item in button_old_list:
                membership = Membership.objects.filter(button_id=item, page=page)
                membership.delete()
            # for key, value in request.POST.items():
            #     print(key)
            #     if key.split('_')[0] == 'button':
            #         button_id = key.split('_')[1]
            #         if button_old_list.count(int(button_id)):
            #             button_old_list.remove(int(button_id))
            #         button = Button.objects.get(pk=button_id)
            #         membership = Membership.objects.update_or_create(page=page, button=button)
            # for item in button_old_list:
            #     membership = Membership.objects.filter(button_id=item, page=page)
            #     membership.delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '分配成功!'}))
        else:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '页面编号丢失，请重新刷新后重试!'}))
