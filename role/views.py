from django.db.models import DateTimeField, CharField
from django.db.models.functions import Cast, TruncSecond
from django.shortcuts import render
from .models import Role, RolesButton
from .forms import RoleAddForm, RoleEditForm
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
import json
from button.models import Button, Membership
from page.models import Page


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        try:
            page_code = Page.objects.get(menu_code='role').id
            button = Button.objects.filter(membership__rolesbutton__role_id=request.user.role.id,
                                           membership__page_id=page_code)
            button_external = list(button.filter(button_type=2).values('button_name', 'button_code', 'button_icon'))
            button_internal = list(button.filter(button_type=1).values('button_name', 'button_code', 'button_icon'))
            return render(request, 'role/index.html',
                          {'button_external': button_external, 'button_internal': button_internal})
        except Page.DoesNotExist:
            return HttpResponseNotFound()


def role_list(request):
    if request.method == 'GET':
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        begin = (page - 1) * limit
        end = begin + limit - 1

        role_item = Role.objects.all().extra(
            select={"create_time": "DATE_FORMAT(create_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
                    "update_time": "DATE_FORMAT(update_time, '%%Y-%%m-%%d %%H:%%i:%%s')"}).values('id', 'role_name',
                                                                                                  'create_time',
                                                                                                  'update_time',
                                                                                                  'status')[
                    begin:end]

        return_msg = {
            "code": 0,
            "msg": "",
            "count": role_item.count(),
            "data": list(role_item)
        }
        print(return_msg)

        return HttpResponse(json.dumps(return_msg, indent=4, sort_keys=True, default=str))


def add_role(request):
    if request.method == 'GET':
        role_form = RoleAddForm()
        return render(request, 'role/add.html', {'form': role_form})
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
            role_form = RoleEditForm(instance=role)
            return render(request, 'role/edit.html', {'form': role_form, 'role_id': role.id})
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


def roles_button(request):
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        if role_id:
            return render(request, 'role/roles_button.html', {'role_id': role_id})
        else:
            return HttpResponseNotFound()
    else:
        role_id = request.POST.get('role_id')
        menu_list = request.POST.get('list')
        role = Role.objects.get(pk=role_id)

        # print(menu_list)
        if role_id and menu_list:
            old_role_button = list(Membership.objects.filter(rolesbutton__role_id=role_id).values_list('id',
                                                                                                       flat=True))
            for i in eval(menu_list):
                temp = Membership.objects.filter(rolesbutton__role_id=role_id, button_id=int(i['ActionId']),
                                                 page_id=int(i['MenuId']))
                if temp.count():
                    old_role_button.remove(int(temp.first().id))
                else:
                    membership = Membership.objects.get(button_id=i['ActionId'], page_id=i['MenuId'])
                    RolesButton.objects.create(button=membership, role=role)
            for i in old_role_button:
                RolesButton.objects.filter(button_id=i).delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '分配按钮成功!'}))
        elif menu_list is None and role_id is not None:
            RolesButton.objects.filter(role_id=role_id).delete()
        else:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '角色编号丢失，请刷新后重试!'}))
        return HttpResponse(json.dumps({'state': 'success', 'message': '添加成功'}))


def role_page_button(request):
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        item_list = []
        item_all = Page.objects.all()

        for item in item_all:
            button_html = ''
            role_button = list(
                Membership.objects.filter(rolesbutton__role_id=role_id, page_id=item.id).values_list('button_id',
                                                                                                     flat=True))
            button = Button.objects.filter(membership__page_id=item.id)

            for i in button:
                if i.id in role_button:
                    button_html += "<input name='cbx_{0}' value='{1}' " \
                                   "title='{2}' type='checkbox' checked='' style='margin-right:5px'>".format(item.id,
                                                                                                             i.id,
                                                                                                             i.button_name)
                else:
                    button_html += "<input name='cbx_{0}' value='{1}' " \
                                   "title='{2}' type='checkbox' style='margin-right:5px'>".format(item.id, i.id,
                                                                                                  i.button_name)
            dic = {'id': item.id, 'menu_name': item.menu_name, 'menu_url': item.menu_url,
                   'create_time': item.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                   'status': item.status, 'order_no': item.order_no,
                   'button': button_html,
                   'IsChecked': 'true' if len(role_button) else 'false',
                   'parent_id': item.parent_id if item.parent_id else 0}
            print(dic)
            item_list.append(dic)

        return HttpResponse(json.dumps(
            {'code': 0, 'msg': '', 'data': item_list, 'count': len(item_list), 'is': 'true', 'tips': '操作成功!'}, indent=4,
            sort_keys=True, default=str))
