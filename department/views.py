from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department
from django.http import HttpResponse, Http404
import json
from .forms import DepartmentCreateForm, DepartmentEditForm
from django.core.exceptions import ObjectDoesNotExist
from page.models import Page
from button.models import Button


# Create your views here.
def get_department(department_code):
    list_children = Department.objects.all().filter(parent_department=department_code)
    list_children_item = []

    for item in list_children:
        dic = {'id': item.department_code, 'title': item.department_name,
               'parentId': department_code if department_code else 0,
               'children': get_department(item.department_code)}
        list_children_item.append(dic)

    return list_children_item


def index_view(request):
    if request.method == 'GET':
        page_code = Page.objects.get(menu_code='department').id
        button = list(Button.objects.filter(membership__rolesbutton__role_id=request.user.role.id,
                                            membership__page_id=page_code).values('button_name', 'button_code',
                                                                                  'button_icon'))
        return render(request, 'department/index.html', {'button_list': button})


def department_list(request):
    if request.method == 'GET':
        return_data = {'code': 0, 'msg': '获取成功', 'data': get_department(None)}

        return HttpResponse(json.dumps(return_data))


def create_view(request):
    if request.method == 'GET':
        parent_department = request.GET.get('parent_department')
        return render(request, 'department/add.html', {'parent_department': parent_department})


def create_department(request):
    if request.is_ajax():
        department = DepartmentCreateForm(request.POST)
        if department.is_valid():
            print(request.POST)
            if request.POST['parent_department'] > '0':
                try:
                    parent_department = Department.objects.get(pk=request.POST['parent_department'])
                    new_department = department.save(commit=False)
                    new_department.parent_department = parent_department
                    new_department.save()

                    return HttpResponse(json.dumps({'state': 'success', 'message': '创建成功!'}))
                except ObjectDoesNotExist:
                    return HttpResponse(json.dumps({'state': 'fail', 'message': '上级部门不存在,请重试!'}))
            else:
                department.save()
                return HttpResponse(json.dumps({'state': 'success', 'message': '创建成功!'}))
        else:
            return HttpResponse(json.dumps({'state': 'fail', 'message': department.errors}))


def edit_department(request):
    if request.method == 'GET':
        department = get_object_or_404(Department, pk=request.GET.get('parent_department'))
        form = DepartmentEditForm(instance=department)

        return render(request, 'department/edit.html', {'form': form})
    else:
        department_code = request.POST.get('department_code')
        if department_code == request.POST.get('parent_department'):
            return HttpResponse(json.dumps({'state': 'fail', 'message': '上级部门不能为自身，请重试!'}))
        else:
            try:
                department = Department.objects.get(department_code=department_code)
                form = DepartmentEditForm(request.POST, instance=department)
                if form.is_valid():
                    form.save()
                    return HttpResponse(json.dumps({'state': 'success', 'message': '档案编辑成功!'}))
                else:
                    return HttpResponse(json.dumps({'state': 'fail', 'message': form.errors}))
            except Department.DoesNotExist:
                return HttpResponse(json.dumps({'state': 'fail', 'message': '当前编辑的部门已丢失，请刷新后重试!'}))


def del_department(request):
    department_code = request.POST.get('department')
    if department_code:
        try:
            department = Department.objects.get(pk=department_code)
            department.delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '删除成功!'}))
        except Department.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '想要删除的部门不存在，请重试!'}))
    else:
        return HttpResponse(json.dumps({'state': 'fail', 'message': '当前服务器接收到的部门编号为空，请重试!'}))
