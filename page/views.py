from django.shortcuts import render
from .models import Page
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
import json
from button.models import Button
from .forms import PageAddForm, PageEditForm


def get_page_list(page_id):
    list_children = Page.objects.all().filter(parent_id=page_id)
    list_children_item = []

    for item in list_children:
        dic = {'id': item.id, 'title': item.menu_name,
               'parentId': page_id if page_id else 0,
               'children': get_page_list(item.id)}
        list_children_item.append(dic)

    return list_children_item


def page_tree(request):
    if request.method == 'GET':
        data = get_page_list(None)
        # data.append({'id': -1, 'title': '导航界面', 'parentId': 0, 'children': []})
        return HttpResponse(json.dumps({'code': 0, 'msg': '获取成功', 'data': data}))


def index_view(request):
    """
    返回菜单页面首页
    :param request:
    :return: 网页视图
    """
    if request.method == 'GET':
        try:
            page_code = Page.objects.get(menu_code='page').id
            button = Button.objects.filter(membership__rolesbutton__role_id=request.user.role.id,
                                           membership__page_id=page_code)
            button_external = list(button.filter(button_type=2).values('button_name', 'button_code', 'button_icon'))
            button_internal = list(button.filter(button_type=1).values('button_name', 'button_code', 'button_icon'))
            print(button_internal)
            return render(request, 'page/index.html',
                          {'button_external': button_external, 'button_internal': button_internal})
        except Page.DoesNotExist:
            return HttpResponseNotFound()


def page_list(request):
    """
    获取界面列表源数据
    :param request:
    :return: GET-{'code': 0, 'msg': '', 'data': item_list, 'count': len(item_list), 'is': 'true', 'tips': '操作成功!'}
    """
    if request.method == 'GET':
        item_list = []
        item_all = Page.objects.all()

        for item in item_all:
            dic = {'id': item.id, 'menu_name': item.menu_name, 'menu_url': item.menu_url,
                   'menu_code': item.menu_code,
                   'create_time': item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                   'status': item.status, 'order_no': item.order_no,
                   'menu_icon': item.menu_icon,
                   'button': ','.join(
                       list(Button.objects.filter(membership__page_id=item.id).values_list('button_name', flat=True))),
                   'parent_id': item.parent_id if item.parent_id else 0}

            item_list.append(dic)
        print(item_list)
        return HttpResponse(json.dumps(
            {'code': 0, 'msg': '', 'data': item_list, 'count': len(item_list), 'is': 'true', 'tips': '操作成功!'}, indent=4,
            sort_keys=True, default=str))


def del_page(request):
    """
    根据传进来的id删除对应的page记录
    :param request:
    :return: POST-记录存在-{'state': 'success', 'message': '删除成功'}
                  记录不存在-{'state': 'fail', 'message': '删除的页面不存在，请刷新后重试!'}
    """
    if request.method == 'POST':
        page_id = request.POST.get('id')
        try:
            page = Page.objects.get(pk=page_id)
            page.delete()
            return HttpResponse(json.dumps({'state': 'success', 'message': '删除成功'}))
        except Page.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '删除的页面不存在，请刷新后重试!'}))


def edit_page(request):
    if request.method == 'POST':
        page_id = request.POST.get('id')
        try:
            if page_id == request.POST.get('parent'):
                return HttpResponse(json.dumps({'state': 'fail', 'message': '上级界面不能为自身，请重试!'}))
            else:
                page = Page.objects.get(pk=page_id)
                form = PageAddForm(request.POST, instance=page)
                if form.is_valid():
                    form.save()
                    return HttpResponse(json.dumps({'state': 'success', 'message': '编辑成功'}))
                else:
                    print(form.errors)
                    return HttpResponse(json.dumps({'state': 'fail', 'message': form.errors}))
        except Page.DoesNotExist:
            return HttpResponse(json.dumps({'state': 'fail', 'message': '当前编辑界面数据丢失，请刷新后重试!'}))
    else:
        page_id = request.GET.get('id')
        page = get_object_or_404(Page, pk=page_id)
        form = PageEditForm(instance=page)
        print(form)
        return render(request, 'page/edit.html', {'form': form, 'id': page_id})


def add_page(request):
    if request.method == 'GET':
        form = PageAddForm()
        return render(request, 'page/add.html', {'form': form})
    else:
        page_form = PageAddForm(request.POST)
        if page_form.is_valid():
            page = page_form.save()
            return HttpResponse(json.dumps({'state': 'success', 'message': '添加成功'}))
        else:
            print(page_form.errors)
            return HttpResponse(json.dumps({'state': 'fail', 'message': page_form.errors}))
