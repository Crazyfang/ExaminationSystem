from django.shortcuts import render
from .models import Role
from .forms import RoleAddForm, RoleEditForm
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
import json


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, '')


def role_list(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        begin = (page - 1) * limit
        end = begin + limit - 1

        role_item = Role.objects.all().values('id', 'role_name')[begin:end]

        return_msg = {
            "code": 0,
            "msg": "",
            "count": role_item.count(),
            "data": list(role_item)
        }
        print(return_msg)

        return HttpResponse(json.dumps(return_msg))


def add_role(request):
    if request.method == 'GET':
        return render(request, '')
    else:
        form = RoleAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'state': 'success', 'message': '添加成功!'}))
        else:
            return HttpResponse(json.dumps({'state': 'fail', 'message': form.errors}))


def edit_role(request):
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        try:
            role = get_object_or_404(Role, pk=role_id)
            return render(request, '', {'form': role})
        except Http404:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '编辑的角色不存在，请刷新后重试!'}))
    else:
        role_id = request.POST.get('id')
        try:
            role = Role.objects.get(pk=role_id)
            form = RoleEditForm(request.POST, instance=role)
            if form.is_valid():
                form.save()
                return HttpResponse(json.dumps({'state': 'success', 'message': '编辑成功!'}))
            else:
                return HttpResponse(json.dumps({'state': 'fail', 'message': form.errors}))
        except Role.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '编辑的角色不存在，请刷新后重试!'}))


def del_role(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')
        try:
            role = Role.objects.get(pk=role_id)
            role.delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '删除成功!'}))
        except Role.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '删除的角色不存在，请刷新后重试!'}))