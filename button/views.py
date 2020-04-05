from django.shortcuts import render
from .models import Button
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .forms import ButtonEditForm, ButtonAddForm
import json


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'button/index.html')


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

        button_value = Button.objects.all().values('id', 'button_name', 'button_type', 'create_time', 'status')[
                       begin:end]

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
