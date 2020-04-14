from django.shortcuts import render
from role.models import RolesButton
from button.models import Membership
from page.models import Page


# from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.


# TODO 完善首页页面导航的展示  按钮添加button_code  界面添加page_code  界面中的按钮自动生成  母页不允许添加按钮


def index_view(request):
    page_list = []
    page_show = Page.objects.filter(membership__rolesbutton__role_id=request.user.role.id).distinct()
    page_head = Page.objects.filter(parent_id=None)

    for head_page in page_head:
        if page_show.filter(parent_id=head_page.id).count():
            dic_children = []
            for children_page in page_show.filter(parent_id=head_page.id):
                dic = {'menu_name': children_page.menu_name, 'menu_url': children_page.menu_url,
                       'menu_code': children_page.menu_code, 'menu_icon': children_page.menu_icon}
                dic_children.append(dic)
            dic = {'menu_name': head_page.menu_name, 'menu_url': head_page.menu_url, 'menu_code': head_page.menu_code,
                   'children_page': dic_children, 'menu_icon': head_page.menu_icon}
            page_list.append(dic)
        else:
            pass

    return render(request, 'home/index.html', {'user': request.user, 'page_list': page_list})


def console_view(request):
    return render(request, 'home/console.html')
