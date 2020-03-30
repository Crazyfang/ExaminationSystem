from django.shortcuts import render
from .models import Department
from django.http import HttpResponse
import json
from .forms import DepartmentCreateForm
from django.core.exceptions import ObjectDoesNotExist


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
        return render(request, 'department/index.html')


def department_list(request):
    if request.method == 'POST':
        return_data = {'code': 0, 'msg': '获取成功', 'data': get_department(None)}

        return HttpResponse(json.dumps(return_data))


def create_view(request, parent_department):
    if request.method == 'GET':
        return render(request, 'department/add_department.html', {'parent_department': parent_department})


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



